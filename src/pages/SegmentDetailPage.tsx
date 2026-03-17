import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { getSegment, validateSegment } from "../api/segments";
import { SegmentDetail } from "../types";

export default function SegmentDetailPage() {
  const params = useParams();
  const [segment, setSegment] = useState<SegmentDetail | null>(null);

  async function load() {
    if (!params.id) return;
    setSegment(await getSegment(Number(params.id)));
  }

  useEffect(() => {
    load();
  }, [params.id]);

  if (!segment) {
    return <div className="panel">Cargando detalle...</div>;
  }

  return (
    <section className="stack">
      <div className="split-header">
        <div>
          <h2>{segment.name}</h2>
          <p>
            {segment.cidr} | {segment.network_type} | {segment.status}
          </p>
        </div>
        <button type="button" onClick={() => validateSegment(segment.id).then(load)}>
          Ejecutar validación manual
        </button>
      </div>

      <div className="grid-two">
        <div className="panel">
          <h3>Ficha técnica</h3>
          <dl className="detail-grid">
            <div>
              <dt>Descripción</dt>
              <dd>{segment.description ?? "-"}</dd>
            </div>
            <div>
              <dt>Ubicación</dt>
              <dd>{segment.location?.name ?? "-"}</dd>
            </div>
            <div>
              <dt>Nodo</dt>
              <dd>{segment.node?.name ?? "-"}</dd>
            </div>
            <div>
              <dt>Equipo</dt>
              <dd>{segment.equipment ?? "-"}</dd>
            </div>
            <div>
              <dt>Pool</dt>
              <dd>{segment.pool?.name ?? "-"}</dd>
            </div>
            <div>
              <dt>IP principal</dt>
              <dd>{segment.primary_validation_ip ?? "-"}</dd>
            </div>
            <div>
              <dt>Última validación</dt>
              <dd>{segment.last_validation_at ?? "Sin ejecutar"}</dd>
            </div>
            <div>
              <dt>Tiempo respuesta</dt>
              <dd>{segment.last_response_time_ms ? `${segment.last_response_time_ms} ms` : "-"}</dd>
            </div>
          </dl>
        </div>

        <div className="panel">
          <h3>Estado actual</h3>
          <div className="status-row">
            <span
              className={
                segment.last_ping_ok === null || segment.last_ping_ok === undefined ? "badge" : segment.last_ping_ok ? "badge ok" : "badge fail"
              }
            >
              Ping: {segment.last_ping_ok === null || segment.last_ping_ok === undefined ? "N/A" : segment.last_ping_ok ? "OK" : "FAIL"}
            </span>
            <span
              className={
                segment.last_snmp_ok === null || segment.last_snmp_ok === undefined ? "badge" : segment.last_snmp_ok ? "badge ok" : "badge fail"
              }
            >
              SNMP: {segment.last_snmp_ok === null || segment.last_snmp_ok === undefined ? "N/A" : segment.last_snmp_ok ? "OK" : "FAIL"}
            </span>
          </div>
          <p>{segment.last_validation_error ?? "Sin errores registrados."}</p>
        </div>
      </div>

      <div className="grid-two">
        <div className="panel">
          <h3>Historial de validaciones</h3>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Fecha</th>
                  <th>IP</th>
                  <th>Ping</th>
                  <th>SNMP</th>
                  <th>Tiempo</th>
                  <th>Error</th>
                </tr>
              </thead>
              <tbody>
                {segment.validations.map((item) => (
                  <tr key={item.id}>
                    <td>{new Date(item.created_at).toLocaleString()}</td>
                    <td>{item.validation_ip}</td>
                    <td>{item.ping_ok ? "OK" : "FAIL"}</td>
                    <td>{item.snmp_ok ? "OK" : "FAIL"}</td>
                    <td>{item.response_time_ms ?? "-"}</td>
                    <td>{item.error_message ?? "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        <div className="panel">
          <h3>Auditoría</h3>
          <div className="timeline">
            {segment.audits.map((audit) => (
              <div key={audit.id} className="timeline-item">
                <strong>{audit.action}</strong>
                <span>{audit.details ?? "-"}</span>
                <small>{new Date(audit.created_at).toLocaleString()}</small>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
