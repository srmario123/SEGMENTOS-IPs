export type User = {
  id: number;
  username: string;
  full_name: string;
  email: string;
  role: "admin" | "operator" | "viewer";
  is_active: boolean;
};

export type Catalog = {
  id: number;
  name: string;
  description?: string | null;
};

export type Segment = {
  id: number;
  name: string;
  cidr: string;
  network_address: string;
  prefix_length: number;
  network_type: "public" | "private";
  description?: string | null;
  vlan?: string | null;
  equipment?: string | null;
  status: "active" | "in_use" | "reserved" | "free" | "disabled";
  observations?: string | null;
  is_pool_member: boolean;
  pool_id?: number | null;
  location_id?: number | null;
  node_id?: number | null;
  primary_validation_ip?: string | null;
  scan_multiple_ips: boolean;
  validation_frequency_minutes: number;
  snmp_community?: string | null;
  last_ping_ok?: boolean | null;
  last_snmp_ok?: boolean | null;
  last_validation_at?: string | null;
  last_response_time_ms?: number | null;
  last_validation_error?: string | null;
  pool?: Catalog | null;
  location?: Catalog | null;
  node?: Catalog | null;
};

export type SegmentDetail = Segment & {
  validations: ValidationRecord[];
  audits: AuditRecord[];
};

export type ValidationRecord = {
  id: number;
  validation_ip: string;
  ping_ok: boolean;
  snmp_ok: boolean;
  response_time_ms?: number | null;
  error_message?: string | null;
  validated_by: string;
  created_at: string;
};

export type AuditRecord = {
  id: number;
  action: string;
  details?: string | null;
  created_at: string;
  user_id?: number | null;
};

export type Dashboard = {
  total_segments: number;
  public_segments: number;
  private_segments: number;
  active_segments: number;
  inactive_segments: number;
  validation_ok: number;
  ping_fail: number;
  snmp_fail: number;
  overlap_alerts: string[];
};
