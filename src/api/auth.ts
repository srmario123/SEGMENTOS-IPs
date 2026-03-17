import api from "./client";
import { User } from "../types";

export async function login(username: string, password: string) {
  const { data } = await api.post("/auth/login", { username, password });
  return data as { access_token: string; username: string; role: string };
}

export async function getMe() {
  const { data } = await api.get("/auth/me");
  return data as User;
}
