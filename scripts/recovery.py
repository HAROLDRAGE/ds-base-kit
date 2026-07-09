#!/usr/bin/env python3
"""
🔄 SISTEMA DE RECOVERY Y ROLLBACK
Recuperación automática y reversión de cambios

Funciones:
1. Backup automático del sistema
2. Snapshots de estado
3. Rollback a versión anterior
4. Recovery de cambios perdidos
5. Histórico de cambios

Uso: python3 scripts/recovery.py [--backup] [--restore] [--snapshot] [--status] [--list-backups]
"""

import shutil
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Optional
import sys

class RecoveryManager:
    def __init__(self, workspace_root="."):
        self.root = Path(workspace_root)
        self.backups_dir = self.root / ".backups"
        self.snapshots_file = self.root / ".snapshots"
        
        # Crear directorio de backups
        self.backups_dir.mkdir(exist_ok=True)
        
        self.critical_dirs = [
            "01-tokens",
            "02-componentes",
            "03-patrones",
            "05-agentes",
            "assets"
        ]
        
        self.critical_files = [
            "index.html",
            "README.md",
            "CLAUDE.md",
            "VERSION"
        ]
    
    def create_backup(self, label: Optional[str] = None) -> bool:
        """Crear backup completo del sistema"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        label = label or "auto"
        backup_dir = self.backups_dir / f"backup-{label}-{timestamp}"
        
        print(f"\n💾 CREANDO BACKUP: {backup_dir.name}")
        print("=" * 60)
        
        try:
            backup_dir.mkdir(exist_ok=True)
            
            # Backup de directorios críticos
            for dir_name in self.critical_dirs:
                source = self.root / dir_name
                if source.exists():
                    dest = backup_dir / dir_name
                    shutil.copytree(source, dest)
                    print(f"✓ Backup: {dir_name}")
            
            # Backup de archivos críticos
            for file_name in self.critical_files:
                source = self.root / file_name
                if source.exists():
                    dest = backup_dir / file_name
                    shutil.copy2(source, dest)
                    print(f"✓ Backup: {file_name}")
            
            # Guardar metadata
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "label": label,
                "version": self._get_version(),
                "files_count": sum(1 for _ in backup_dir.rglob("*") if _.is_file())
            }
            
            (backup_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))
            
            print(f"\n✅ Backup creado exitosamente")
            print(f"Ubicación: {backup_dir}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error creando backup: {e}")
            return False
    
    def restore_backup(self, backup_name: Optional[str] = None) -> bool:
        """Restaurar desde backup"""
        print(f"\n🔄 RESTAURANDO DESDE BACKUP")
        print("=" * 60)
        
        # Listar backups disponibles
        backups = list(self.backups_dir.glob("backup-*"))
        
        if not backups:
            print("✗ No hay backups disponibles")
            return False
        
        # Si no se especifica, usar el más reciente
        if not backup_name:
            backup_dir = max(backups, key=lambda x: x.stat().st_mtime)
        else:
            backup_dir = self.backups_dir / backup_name
        
        if not backup_dir.exists():
            print(f"✗ Backup no encontrado: {backup_name}")
            return False
        
        print(f"Restaurando desde: {backup_dir.name}")
        
        try:
            # Restaurar directorios
            for dir_name in self.critical_dirs:
                source = backup_dir / dir_name
                dest = self.root / dir_name
                
                if source.exists():
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(source, dest)
                    print(f"✓ Restaurado: {dir_name}")
            
            # Restaurar archivos
            for file_name in self.critical_files:
                source = backup_dir / file_name
                dest = self.root / file_name
                
                if source.exists():
                    if dest.exists():
                        dest.unlink()
                    shutil.copy2(source, dest)
                    print(f"✓ Restaurado: {file_name}")
            
            print(f"\n✅ Restauración completada")
            return True
            
        except Exception as e:
            print(f"✗ Error restaurando: {e}")
            return False
    
    def create_snapshot(self, name: str) -> bool:
        """Crear snapshot del estado actual"""
        print(f"\n📸 CREANDO SNAPSHOT: {name}")
        print("=" * 60)
        
        snapshots = {}
        
        # Cargar snapshots anteriores
        if self.snapshots_file.exists():
            snapshots = json.loads(self.snapshots_file.read_text())
        
        # Crear snapshot
        snapshot = {
            "name": name,
            "timestamp": datetime.now().isoformat(),
            "version": self._get_version(),
            "checksums": self._calculate_checksums()
        }
        
        snapshots[name] = snapshot
        
        # Guardar
        self.snapshots_file.write_text(json.dumps(snapshots, indent=2))
        
        print(f"✅ Snapshot '{name}' creado")
        return True
    
    def compare_snapshot(self, snapshot_name: str) -> dict:
        """Comparar con un snapshot anterior"""
        snapshots = {}
        
        if self.snapshots_file.exists():
            snapshots = json.loads(self.snapshots_file.read_text())
        
        if snapshot_name not in snapshots:
            print(f"✗ Snapshot no encontrado: {snapshot_name}")
            return {}
        
        old_snapshot = snapshots[snapshot_name]
        current_checksums = self._calculate_checksums()
        
        changes = {
            "added": [],
            "removed": [],
            "modified": []
        }
        
        for file, checksum in current_checksums.items():
            if file not in old_snapshot["checksums"]:
                changes["added"].append(file)
            elif old_snapshot["checksums"][file] != checksum:
                changes["modified"].append(file)
        
        for file in old_snapshot["checksums"]:
            if file not in current_checksums:
                changes["removed"].append(file)
        
        return changes
    
    def status(self) -> dict:
        """Mostrar estado del sistema de recovery"""
        backups = list(self.backups_dir.glob("backup-*"))
        snapshots = {}
        
        if self.snapshots_file.exists():
            snapshots = json.loads(self.snapshots_file.read_text())
        
        status = {
            "backups_count": len(backups),
            "snapshots_count": len(snapshots),
            "latest_backup": None,
            "total_backup_size": 0
        }
        
        if backups:
            latest = max(backups, key=lambda x: x.stat().st_mtime)
            status["latest_backup"] = latest.name
            
            # Calcular tamaño total
            total_size = sum(f.stat().st_size for f in latest.rglob("*") if f.is_file())
            status["total_backup_size"] = round(total_size / 1024 / 1024, 2)  # MB
        
        return status
    
    def list_backups(self) -> List[dict]:
        """Listar todos los backups disponibles"""
        backups = []
        
        for backup_dir in sorted(self.backups_dir.glob("backup-*"), reverse=True):
            metadata_file = backup_dir / "metadata.json"
            
            if metadata_file.exists():
                metadata = json.loads(metadata_file.read_text())
            else:
                metadata = {"label": "unknown", "timestamp": "unknown"}
            
            size = sum(f.stat().st_size for f in backup_dir.rglob("*") if f.is_file())
            
            backups.append({
                "name": backup_dir.name,
                "label": metadata.get("label"),
                "timestamp": metadata.get("timestamp"),
                "size_mb": round(size / 1024 / 1024, 2),
                "version": metadata.get("version")
            })
        
        return backups
    
    def cleanup_old_backups(self, keep_count: int = 5) -> int:
        """Limpiar backups antiguos"""
        backups = sorted(self.backups_dir.glob("backup-*"), key=lambda x: x.stat().st_mtime)
        
        if len(backups) <= keep_count:
            return 0
        
        to_remove = backups[:-keep_count]
        removed_count = 0
        
        for backup in to_remove:
            shutil.rmtree(backup)
            removed_count += 1
            print(f"🗑️  Eliminado: {backup.name}")
        
        return removed_count
    
    def _calculate_checksums(self) -> dict:
        """Calcular checksums de archivos críticos"""
        checksums = {}
        
        for file_path in self.root.rglob("*"):
            if not file_path.is_file():
                continue
            
            # Solo archivos críticos
            rel_path = str(file_path.relative_to(self.root))
            
            skip = False
            for pattern in [".git", "__pycache__", ".backups", "logs"]:
                if pattern in rel_path:
                    skip = True
                    break
            
            if skip:
                continue
            
            try:
                hash_obj = hashlib.sha256()
                with open(file_path, "rb") as f:
                    hash_obj.update(f.read())
                checksums[rel_path] = hash_obj.hexdigest()
            except:
                pass
        
        return checksums
    
    def _get_version(self) -> str:
        """Obtener versión actual"""
        version_file = self.root / "VERSION"
        if version_file.exists():
            return version_file.read_text().strip()
        return "unknown"


def main():
    backup = "--backup" in sys.argv
    restore = "--restore" in sys.argv
    snapshot = "--snapshot" in sys.argv
    status = "--status" in sys.argv
    list_backups = "--list-backups" in sys.argv
    cleanup = "--cleanup" in sys.argv
    
    manager = RecoveryManager()
    
    print("\n🔄 GESTOR DE RECOVERY Y ROLLBACK")
    print("=" * 60)
    
    if backup:
        manager.create_backup()
    
    if restore:
        manager.restore_backup()
    
    if snapshot:
        # Buscar argumento de nombre
        snapshot_name = "auto"
        for i, arg in enumerate(sys.argv):
            if arg == "--snapshot" and i + 1 < len(sys.argv):
                snapshot_name = sys.argv[i + 1]
                break
        manager.create_snapshot(snapshot_name)
    
    if status:
        status_info = manager.status()
        print("\n📊 Estado del Sistema:")
        print(f"  Backups: {status_info['backups_count']}")
        print(f"  Snapshots: {status_info['snapshots_count']}")
        print(f"  Último backup: {status_info['latest_backup']}")
        print(f"  Tamaño: {status_info['total_backup_size']} MB")
    
    if list_backups:
        backups = manager.list_backups()
        print("\n📋 Backups Disponibles:")
        for backup in backups:
            print(f"\n  {backup['name']}")
            print(f"    Label: {backup['label']}")
            print(f"    Timestamp: {backup['timestamp']}")
            print(f"    Tamaño: {backup['size_mb']} MB")
            print(f"    Versión: {backup['version']}")
    
    if cleanup:
        removed = manager.cleanup_old_backups()
        print(f"✅ Eliminados {removed} backups antiguos")


if __name__ == "__main__":
    main()
