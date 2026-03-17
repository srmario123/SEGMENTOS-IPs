import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin123");
  const [error, setError] = useState("");

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    try {
      setError("");
      await login(username, password);
      navigate("/");
    } catch {
      setError("No fue posible iniciar sesión");
    }
  }

  return (
    <div className="login-shell">
      <form className="login-card" onSubmit={handleSubmit}>
        <h1>IP Segment Manager</h1>
        <p>Plataforma NOC para inventario y validación de segmentos IPv4.</p>
        <label>
          Usuario
          <input value={username} onChange={(e) => setUsername(e.target.value)} required />
        </label>
        <label>
          Contraseña
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        {error ? <div className="alert error">{error}</div> : null}
        <button type="submit">Ingresar</button>
      </form>
    </div>
  );
}
