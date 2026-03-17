import api from "./client";
import { Dashboard, Segment, SegmentDetail, ValidationRecord } from "../types";

export async function getDashboard() {
  const { data } = await api.get("/segments/dashboard");
  return data as Dashboard;
}

export async function getSegments(params?: Record<string, string | number | undefined>) {
  const { data } = await api.get("/segments", { params });
  return data as { items: Segment[]; total: number; overlap_alerts: string[] };
}

export async function getSegment(id: number) {
  const { data } = await api.get(`/segments/${id}`);
  return data as SegmentDetail;
}

export async function createSegment(payload: Record<string, unknown>) {
  const { data } = await api.post("/segments", payload);
  return data as Segment;
}

export async function updateSegment(id: number, payload: Record<string, unknown>) {
  const { data } = await api.put(`/segments/${id}`, payload);
  return data as Segment;
}

export async function deleteSegment(id: number) {
  await api.delete(`/segments/${id}`);
}

export async function validateSegment(id: number, validation_ip?: string, scan_multiple_ips = false) {
  const { data } = await api.post(`/segments/${id}/validate`, { validation_ip, scan_multiple_ips });
  return data as ValidationRecord[];
}
