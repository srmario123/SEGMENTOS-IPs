import { useEffect, useState } from "react";

import { Catalog, Segment } from "../types";

type Props = {
  locations: Catalog[];
  nodes: Catalog[];
  pools: Catalog[];
  initialValue?: Segment | null;
  onSubmit: (payload: Record<string, unknown>) => Promise<void>;
};

const defaultForm = {
  name: "",
  cidr: "",
  network_type: "private",
  description: "",
  vlan: "",
  equipment: "",
  status: "active",
  observations: "",
  is_pool_member: false,
  pool_id: "",
  location_id: "",
  node_id: "",
  primary_validation_ip: "",
  scan_multiple_ips: false,
  validation_frequency_minutes: 15,
  snmp_community: ""
};

export default function SegmentForm({ locations, nodes, pools, initialValue, onSubmit }: Props) {
  const [form, setForm] = useState(defaultForm);

  useEffect(() => {
    if (!initialValue) {
      setForm(defaultForm);
      return;
    }
    setForm({
      ...defaultForm,
      ...initialValue,
      pool_id: initialValue.pool_id ?? "",
      location_id: initialValue.location_id ?? "",
      node_id: initialValue.node_id ?? ""
    });
  }, [initialValue]);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    await onSubmit({
      ...form,
      pool_id: form.pool_id || null,
      location_id: form.location_id || null,
      node_id: form.node_id || null,
      primary_validation_ip: form.primary_validation_ip || null,
      snmp_community: form.snmp_community || null
    });
    if (!initialValue) {
      setForm(defaultForm);
    }
  }

  return (
    <form className="panel form-grid" onSubmit={handleSubmit}>
      <h3>{initialValue ? "Editar segmento" : "Nuevo segmento"}</h3>
      <label>
        Nombre
        <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
      </label>
      <label>
        CIDR
        <input value={form.cidr} onChange={(e) => setForm({ ...form, cidr: e.target.value })} required />
      </label>
      <label>
        Tipo
        <select value={form.network_type} onChange={(e) => setForm({ ...form, network_type: e.target.value })}>
          <option value="private">Privado</option>
          <option value="public">Público</option>
        </select>
      </label>
      <label>
        Estado
        <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
          <option value="active">Activo</option>
          <option value="in_use">En uso</option>
          <option value="reserved">Reservado</option>
          <option value="free">Libre</option>
          <option value="disabled">Deshabilitado</option>
        </select>
      </label>
      <label>
        VLAN
        <input value={form.vlan} onChange={(e) => setForm({ ...form, vlan: e.target.value })} />
      </label>
      <label>
        Equipo asociado
        <input value={form.equipment} onChange={(e) => setForm({ ...form, equipment: e.target.value })} />
      </label>
      <label>
        Ubicación
        <select value={String(form.location_id)} onChange={(e) => setForm({ ...form, location_id: e.target.value })}>
          <option value="">Sin asignar</option>
          {locations.map((item) => (
            <option key={item.id} value={item.id}>
              {item.name}
            </option>
          ))}
        </select>
      </label>
      <label>
        Nodo
        <select value={String(form.node_id)} onChange={(e) => setForm({ ...form, node_id: e.target.value })}>
          <option value="">Sin asignar</option>
          {nodes.map((item) => (
            <option key={item.id} value={item.id}>
              {item.name}
            </option>
          ))}
        </select>
      </label>
      <label>
        Pool
        <select value={String(form.pool_id)} onChange={(e) => setForm({ ...form, pool_id: e.target.value })}>
          <option value="">Sin asignar</option>
          {pools.map((item) => (
            <option key={item.id} value={item.id}>
              {item.name}
            </option>
          ))}
        </select>
      </label>
      <label>
        IP principal
        <input
          value={form.primary_validation_ip}
          onChange={(e) => setForm({ ...form, primary_validation_ip: e.target.value })}
        />
      </label>
      <label>
        Frecuencia (min)
        <input
          type="number"
          min="5"
          value={form.validation_frequency_minutes}
          onChange={(e) => setForm({ ...form, validation_frequency_minutes: Number(e.target.value) })}
        />
      </label>
      <label>
        Comunidad SNMP
        <input value={form.snmp_community} onChange={(e) => setForm({ ...form, snmp_community: e.target.value })} />
      </label>
      <label className="full">
        Descripción
        <textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
      </label>
      <label className="full">
        Observaciones
        <textarea value={form.observations} onChange={(e) => setForm({ ...form, observations: e.target.value })} />
      </label>
      <label className="checkbox">
        <input
          type="checkbox"
          checked={form.is_pool_member}
          onChange={(e) => setForm({ ...form, is_pool_member: e.target.checked })}
        />
        Pertenece a pool
      </label>
      <label className="checkbox">
        <input
          type="checkbox"
          checked={form.scan_multiple_ips}
          onChange={(e) => setForm({ ...form, scan_multiple_ips: e.target.checked })}
        />
        Escanear varias IPs
      </label>
      <div className="full actions">
        <button type="submit">{initialValue ? "Guardar cambios" : "Crear segmento"}</button>
      </div>
    </form>
  );
}
