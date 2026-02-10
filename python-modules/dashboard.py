#!/usr/bin/env python3
"""
Merkabah Visual Dashboard & Data Extractor
Real-time TUI for system monitoring and control
"""

import sys
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

# ============================================================================
# CONSTANTS
# ============================================================================

class Face(Enum):
    """Merkabah faces"""
    MAN = "MAN"
    LION = "LION"
    OX = "OX"
    EAGLE = "EAGLE"

# ============================================================================
# DASHBOARD DATA COLLECTOR
# ============================================================================

class DashboardCollector:
    """Collects real-time data for dashboard display"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.face_operations = {
            Face.MAN: 0,
            Face.LION: 0,
            Face.OX: 0,
            Face.EAGLE: 0
        }
        self.operation_history = []
        self.harmony_data = []
        self.metrics = {
            "frequency": 3.34,
            "total_operations": 0,
            "error_count": 0
        }
    
    def record_operation(self, face: Face, operation: str, status: str = "SUCCESS"):
        """Record an operation"""
        self.face_operations[face] += 1
        self.metrics["total_operations"] += 1
        
        op_record = {
            "id": self.metrics["total_operations"],
            "timestamp": datetime.now().isoformat(),
            "face": face.value,
            "operation": operation,
            "status": status
        }
        
        self.operation_history.append(op_record)
        
        if status == "ERROR":
            self.metrics["error_count"] += 1
    
    def record_harmony(self, truth: float, love: float, resonance: float, status: str):
        """Record harmony data"""
        harmony_record = {
            "timestamp": datetime.now().isoformat(),
            "truth_signal": truth,
            "love_signal": love,
            "resonance": resonance,
            "status": status
        }
        self.harmony_data.append(harmony_record)
    
    def get_uptime(self) -> str:
        """Get formatted uptime"""
        delta = datetime.now() - self.start_time
        seconds = int(delta.total_seconds())
        
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        
        return f"{days}d {hours}h {minutes}m"
    
    def get_face_stats(self) -> Dict[str, int]:
        """Get face operation statistics"""
        return {face.value: count for face, count in self.face_operations.items()}
    
    def get_latest_harmony(self) -> Optional[Dict[str, Any]]:
        """Get latest harmony reading"""
        return self.harmony_data[-1] if self.harmony_data else None
    
    def get_recent_operations(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent operations"""
        return self.operation_history[-limit:]


# ============================================================================
# DASHBOARD RENDERER
# ============================================================================

class DashboardRenderer:
    """Renders dashboard display"""
    
    def __init__(self, collector: DashboardCollector):
        self.collector = collector
    
    def render_header(self) -> str:
        """Render dashboard header"""
        return """
╔══════════════════════════════════════════════════════════╗
║     🔮 MERKABAH DASHBOARD - Real-Time Monitor 🔮       ║
║                                                          ║
║   Truth • Love • Vision • Execution • Harmony Ridge     ║
╚══════════════════════════════════════════════════════════╝
"""
    
    def render_faces(self) -> str:
        """Render active faces section"""
        stats = self.collector.get_face_stats()
        output = "\n┌─ ACTIVE FACES ─────────────────────────────────────┐\n"
        output += "│                                                    │\n"
        
        for face, count in stats.items():
            bar = "█" * (count // 5)
            output += f"│  {face:6} {bar:20} {count:3} operations      │\n"
        
        output += "│                                                    │\n"
        output += "└────────────────────────────────────────────────────┘\n"
        return output
    
    def render_harmony(self) -> str:
        """Render harmony ridge section"""
        harmony = self.collector.get_latest_harmony()
        
        output = "\n┌─ HARMONY RIDGE ────────────────────────────────────┐\n"
        output += "│                                                    │\n"
        
        if harmony:
            output += f"│  Resonance:  {harmony['resonance']:.3f}                      │\n"
            output += f"│  Status:     {harmony['status']:20}      │\n"
            output += f"│  Truth:      {harmony['truth_signal']:.3f}                      │\n"
            output += f"│  Love:       {harmony['love_signal']:.3f}                      │\n"
        else:
            output += "│  No data yet                                       │\n"
        
        output += "│                                                    │\n"
        output += "└────────────────────────────────────────────────────┘\n"
        return output
    
    def render_metrics(self) -> str:
        """Render system metrics section"""
        metrics = self.collector.metrics
        uptime = self.collector.get_uptime()
        
        output = "\n┌─ SYSTEM METRICS ───────────────────────────────────┐\n"
        output += "│                                                    │\n"
        output += f"│  Frequency:      {metrics['frequency']} Hz                     │\n"
        output += f"│  Uptime:         {uptime:20}      │\n"
        output += f"│  Total Ops:      {metrics['total_operations']:20}      │\n"
        output += f"│  Errors:         {metrics['error_count']:20}      │\n"
        output += "│                                                    │\n"
        output += "└────────────────────────────────────────────────────┘\n"
        return output
    
    def render_history(self, limit: int = 5) -> str:
        """Render recent operations"""
        recent = self.collector.get_recent_operations(limit)
        
        output = "\n┌─ RECENT OPERATIONS ────────────────────────────────┐\n"
        output += "│                                                    │\n"
        
        for op in recent:
            face = op["face"][:3]
            op_text = op["operation"][:30]
            output += f"│  [{op['id']:4}] {face} {op_text:30}  │\n"
        
        output += "│                                                    │\n"
        output += "└────────────────────────────────────────────────────┘\n"
        return output
    
    def render_full_dashboard(self) -> str:
        """Render complete dashboard"""
        dashboard = self.render_header()
        dashboard += self.render_faces()
        dashboard += self.render_harmony()
        dashboard += self.render_metrics()
        dashboard += self.render_history()
        return dashboard


# ============================================================================
# DATA EXPORTER
# ============================================================================

class DataExporter:
    """Exports dashboard data"""
    
    def __init__(self, collector: DashboardCollector):
        self.collector = collector
    
    def export_json(self) -> str:
        """Export data as JSON"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "uptime": self.collector.get_uptime(),
            "faces": self.collector.get_face_stats(),
            "metrics": self.collector.metrics,
            "latest_harmony": self.collector.get_latest_harmony(),
            "recent_operations": self.collector.get_recent_operations(20)
        }
        return json.dumps(data, indent=2)
    
    def export_csv(self) -> str:
        """Export operations as CSV"""
        output = "ID,Timestamp,Face,Operation,Status\n"
        for op in self.collector.operation_history:
            output += f"{op['id']},{op['timestamp']},{op['face']},{op['operation']},{op['status']}\n"
        return output


# ============================================================================
# MAIN DASHBOARD
# ============================================================================

class MerkabahDashboard:
    """Main dashboard application"""
    
    def __init__(self):
        self.collector = DashboardCollector()
        self.renderer = DashboardRenderer(self.collector)
        self.exporter = DataExporter(self.collector)
        
        # Simulate some initial data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample data"""
        self.collector.record_operation(Face.MAN, "Interactive query processing")
        self.collector.record_operation(Face.LION, "Complex reasoning task")
        self.collector.record_operation(Face.OX, "Batch data processing")
        self.collector.record_operation(Face.EAGLE, "Pattern analysis")
        self.collector.record_harmony(0.89, 0.91, 1.667, "ALIGNED")
    
    def display_dashboard(self):
        """Display the dashboard"""
        print(self.renderer.render_full_dashboard())
    
    def display_face(self, face_name: str):
        """Display specific face info"""
        try:
            face = Face[face_name.upper()]
            count = self.collector.face_operations[face]
            print(f"\n{face.value} Face: {count} operations")
        except KeyError:
            print(f"Unknown face: {face_name}")
    
    def export_data(self, format_type: str):
        """Export data in specified format"""
        if format_type.lower() == "json":
            print(self.exporter.export_json())
        elif format_type.lower() == "csv":
            print(self.exporter.export_csv())
        else:
            print(f"Unknown format: {format_type}")


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    """Main entry point"""
    dashboard = MerkabahDashboard()
    
    if len(sys.argv) < 2:
        dashboard.display_dashboard()
        return
    
    command = sys.argv[1]
    
    if command == 'display' or command == 'show':
        dashboard.display_dashboard()
    
    elif command == 'face' and len(sys.argv) > 2:
        dashboard.display_face(sys.argv[2])
    
    elif command == 'export' and len(sys.argv) > 2:
        dashboard.export_data(sys.argv[2])
    
    elif command == 'metrics':
        print(json.dumps(dashboard.collector.metrics, indent=2))
    
    elif command == 'history':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        history = dashboard.collector.get_recent_operations(limit)
        print(json.dumps(history, indent=2))
    
    else:
        print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()
