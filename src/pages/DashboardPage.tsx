import { useEffect, useState } from "react";

import { getDashboard } from "../api/segments";
import MetricCard from "../components/MetricCard";
import { Dashboard } from "../types";

export default function DashboardPage() {
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);

  useEffect(() => {
    getDashboard().then(setDashboard);
  }, []);

  if (!dashboard) {
    return <div className="panel">Cargando dashboard...</div>;
  }

  return (
    <section className="stack">
      <div>
        <h2>Dashboard operativo</h2>
        <p>Resumen de inventario, validaciones y alertas del entorno.</p>
      </div>
      <div className="metrics-grid">
        <MetricCard title="Total segmentos" value={dashboard.total_segments} />
        <MetricCard title="Públicos" value={dashboard.public_segments} />
        <MetricCard title="Privados" value={dashboard.private_segments} />
        <MetricCard title="Activos / En uso" value={dashboard.active_segments} />
        <MetricCard title="Inactivos" value={dashboard.inactive_segments} />
        <MetricCard title="Validación OK" value={dashboard.validation_ok} />
        <MetricCard title="Ping FAIL" value={dashboard.ping_fail} />
        <MetricCard title="SNMP FAIL" value={dashboard.snmp_fail} />
      </div>
      <div className="panel">
        <h3>Alertas</h3>
        {dashboard.overlap_alerts.length ? (
          dashboard.overlap_alerts.map((alert) => (
            <div key={alert} className="alert warning">
              {alert}
            </div>
          ))
        ) : (
          <p>Sin alertas de superposición.</p>
        )}
      </div>
    </section>
  );
}
