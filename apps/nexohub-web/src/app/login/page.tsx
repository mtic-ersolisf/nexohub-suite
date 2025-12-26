"use client";

import Image from "next/image";
import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";

type LoginResponse = {
  access_token: string;
  token_type?: string;
};

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const emailOk = useMemo(() => {
    // validación simple (MVP)
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
  }, [email]);

  const passwordOk = useMemo(() => password.length >= 8, [password]);

  const canSubmit = emailOk && passwordOk && !loading;

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (!emailOk) return setError("Ingresa un email válido.");
    if (!passwordOk) return setError("La contraseña debe tener mínimo 8 caracteres.");

    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ email: email.trim(), password }),
      });

      // Manejo básico de errores
      if (!res.ok) {
        let msg = "No fue posible iniciar sesión.";
        try {
          const data = await res.json();
          msg = data?.detail || data?.message || msg;
        } catch {
          // ignore
        }
        throw new Error(msg);
      }

      const data = (await res.json()) as LoginResponse;

      if (!data?.access_token) {
        throw new Error("Respuesta inválida: falta access_token.");
      }

      localStorage.setItem("access_token", data.access_token);

      // MVP: redirige a home (o a /dashboard cuando exista)
      router.push("/");
    } catch (err: any) {
      setError(err?.message || "Error inesperado.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-5xl grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Panel marca */}
        <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-8 shadow-glow">
          <div className="flex items-center gap-3">
            <Image
              src="/branding/nexohub.png"
              alt="NexoHub"
              width={56}
              height={56}
              priority
            />
            <div>
              <h1 className="text-2xl font-semibold text-ice">NexoHub Console</h1>
              <p className="text-ice/70">CupoYa • CajaCero</p>
            </div>
          </div>

          <div className="mt-8">
            <h2 className="text-4xl font-bold tracking-tight text-ice">
              Acceso seguro,
              <span className="bg-gradient-to-r from-radarCyan to-cupoGreen bg-clip-text text-transparent">
                {" "}
                operación simple
              </span>
              .
            </h2>
            <p className="mt-3 text-ice/70 leading-relaxed">
              Administra tus módulos con una experiencia moderna y confiable,
              alineada a la identidad azul/verde de la startup.
            </p>
          </div>

          <div className="mt-10 flex items-center gap-4">
            <div className="flex items-center gap-2 rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
              <Image src="/branding/cupoya.png" alt="CupoYa" width={28} height={28} />
              <span className="text-ice/80 text-sm">CupoYa</span>
            </div>
            <div className="flex items-center gap-2 rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
              <Image src="/branding/cajacero.png" alt="CajaCero" width={28} height={28} />
              <span className="text-ice/80 text-sm">CajaCero</span>
            </div>
          </div>

          {/* glow decor */}
          <div className="pointer-events-none absolute -top-24 -right-24 h-64 w-64 rounded-full bg-radarCyan/20 blur-3xl" />
          <div className="pointer-events-none absolute -bottom-24 -left-24 h-64 w-64 rounded-full bg-cupoGreen/20 blur-3xl" />
        </section>

        {/* Card login */}
        <section className="rounded-3xl border border-white/10 bg-white/5 p-8 shadow-glow">
          <h3 className="text-xl font-semibold text-ice">Iniciar sesión</h3>
          <p className="mt-1 text-ice/70 text-sm">
            Ingresa tu correo y contraseña para continuar.
          </p>

          <form onSubmit={onSubmit} className="mt-6 space-y-4">
            <div>
              <label className="block text-sm text-ice/80 mb-2">Email</label>
              <input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                type="email"
                placeholder="tuemail@dominio.com"
                className="w-full rounded-2xl border border-white/10 bg-navy/60 px-4 py-3 text-ice outline-none focus:border-radarCyan/60"
                autoComplete="email"
              />
              {!emailOk && email.length > 3 && (
                <p className="mt-2 text-xs text-mint">Formato de email no válido.</p>
              )}
            </div>

            <div>
              <label className="block text-sm text-ice/80 mb-2">Contraseña</label>
              <input
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                type="password"
                placeholder="••••••••"
                className="w-full rounded-2xl border border-white/10 bg-navy/60 px-4 py-3 text-ice outline-none focus:border-cupoGreen/60"
                autoComplete="current-password"
              />
              {!passwordOk && password.length > 0 && (
                <p className="mt-2 text-xs text-mint">Mínimo 8 caracteres.</p>
              )}
            </div>

            {error && (
              <div className="rounded-2xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-ice">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={!canSubmit}
              className="w-full rounded-2xl px-4 py-3 font-semibold text-navy
                bg-gradient-to-r from-radarCyan to-cupoGreen
                disabled:opacity-50 disabled:cursor-not-allowed
                hover:brightness-110 transition"
            >
              {loading ? "Ingresando..." : "Entrar"}
            </button>

            <p className="text-xs text-ice/60">
              MVP: el token se guarda en <code>localStorage</code>. En producción, lo ideal es
              migrarlo a cookies <code>HttpOnly</code>.
            </p>
          </form>
        </section>
      </div>
    </main>
  );
}

