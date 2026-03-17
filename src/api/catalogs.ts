import api from "./client";
import { Catalog } from "../types";

export async function getLocations() {
  const { data } = await api.get("/locations");
  return data as Catalog[];
}

export async function getNodes() {
  const { data } = await api.get("/nodes");
  return data as Catalog[];
}

export async function getPools() {
  const { data } = await api.get("/pools");
  return data as Catalog[];
}
