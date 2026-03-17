import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getLocations, getNodes, getPools } from "../api/catalogs";
import { createSegment, deleteSegment, getSegments, updateSegment, validateSegment } from "../api/segments";
import SegmentForm from "../components/SegmentForm";
import { Catalog, Segment } from "../types";

export default function SegmentsPage() {
  const [segments, setSegments] = useState<Segment[]>([]);
  const [locations, setLocations] = useState<Catalog[]>([]);
  const [nodes, setNodes] = useState<Catalog[]>([]);
  const [pools, setPools] = useState<Catalog[]>([]);
  const [editing, setEditing] = useState<Segment | null>(null);
  const [search, setSearch] = useState("");
  const [networkType, setNetworkType] = useState("");
  const [status, setStatus] = useState("");
  const [locationId, setLocationId] = useState("");
  const [alerts, setAlerts] = useState<string[]>([]);
  const [error, setError] = useState("");

  async function loadData() {
    const [segmentData, locationData, nodeData, poolData] = await Promise.all([
      getSegments({
        search: search || undefined,
        network_type: networkType || undefined,
        status: status || undefined,
        location_id: locationId || undefined
      }),
      getLocations(),
      getNodes(),
      getPools()
    ]);
    setSegments(segmentData.items);
    setAlerts(segmentData.overlap_alerts);
    setLocations(locationData);
    setNodes(nodeData);
    setPools(poolData);
  }

  useEffect(() => {
    loadData().catch(() => setError("No fue posible cargar los datos"));
  }, []);

  async function handleSave(payload: Record<string, unknown>) {
    setError("");
    try {
      if (editing) {
        await updateSegment(editing.id, payload);
      } else {
        await createSegment(payload);
      }
      setEditing(null);
      await loadData();
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? "Error guardando el segmento");
    }
  }

  async function handleSearch(event: React.FormEvent) {
    event.preventDefault();
    const data = await getSegments({
      search: search || undefined,
      network_type: networkType || undefined,
      status: status || undefined,
      location_id: locationId || undefined
    });
    setSegments(data.items);
    setAlerts(data.overlap_alerts);
  }

  async function handleDelete(id: number) {
    await deleteSegment(id);
    await loadData();
  }

  async function handleValidate(id: number) {
    await validateSegment(id);
    await loadData();
  }

  return (
    <section className="stack">
      <div className="split-header">
        <div>
          <h2>Gestión de segmentos</h2>
          <p>Inventario, filtros, validación operativa y control de superposición.</p>
        </div>
        <form className="search-inline" onSubmit={handleSearch}>
          <input placeholder="Buscar por CIDR, VLAN, equipo..." value={search} onChange={(e) => setSearch(e.target.value)} />
          <select value={networkType} onChange={(e) => setNetworkType(e.target.value)}>
            <option value="">Todos los tipos</option>
            <option value="public">Público</option>
            <option value="private">Privado</option>
          </select>
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="">Todos los estados</option>
            <option value="active">Activo</option>
            <option value="in_use">En uso</option>
            <option value="reserved">Reservado</option>
            <option value="free">Libre</option>
            <option value="disabled">Deshabilitado</option>
          </select>
          <select value={locationId} onChange={(e) => setLocationId(e.target.value)}>
            <option value="">Todas las ubicaciones</option>
            {locations.map((item) => (
              <option key={item.id} value={item.id}>
                {item.name}
              </option>
            ))}
          </select>
          <button type="submit">Buscar</button>
        </form>
      </div>

      {error ? <div className="alert error">{error}</div> : null}
      {alerts.map((alert) => (
        <div key={alert} className="alert warning">
          {alert}
        </div>
      ))}

      <div className="grid-two">
        <SegmentForm locations={locations} nodes={nodes} pools={pools} initialValue={editing} onSubmit={handleSave} />
        <div className="panel">
          <h3>Tabla principal</h3>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>CIDR</th>
                  <th>Tipo</th>
                  <th>Ubicación</th>
                  <th>VLAN</th>
                  <th>Estado</th>
                  <th>Ping</th>
                  <th>SNMP</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {segments.map((segment) => (
                  <tr key={segment.id}>
                    <td>
                      <Link to={`/segments/${segment.id}`}>{segment.name}</Link>
                    </td>
                    <td>{segment.cidr}</td>
                    <td>{segment.network_type}</td>
                    <td>{segment.location?.name ?? "-"}</td>
                    <td>{segment.vlan ?? "-"}</td>
                    <td>{segment.status}</td>
                    <td>
                      <span className={segment.last_ping_ok ? "badge ok" : "badge fail"}>
                        {segment.last_ping_ok === null || segment.last_ping_ok === undefined ? "N/A" : segment.last_ping_ok ? "OK" : "FAIL"}
                      </span>
                    </td>
                    <td>
                      <span className={segment.last_snmp_ok ? "badge ok" : "badge fail"}>
                        {segment.last_snmp_ok === null || segment.last_snmp_ok === undefined ? "N/A" : segment.last_snmp_ok ? "OK" : "FAIL"}
                      </span>
                    </td>
                    <td className="actions-row">
                      <button type="button" className="secondary" onClick={() => setEditing(segment)}>
                        Editar
                      </button>
                      <button type="button" className="secondary" onClick={() => handleValidate(segment.id)}>
                        Validar
                      </button>
                      <button type="button" className="danger" onClick={() => handleDelete(segment.id)}>
                        Eliminar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
}
