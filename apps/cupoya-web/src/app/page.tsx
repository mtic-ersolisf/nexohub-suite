import Image from "next/image";
import { Car, Warehouse } from "lucide-react";

const WHATSAPP_URL =
  "https://wa.me/573003803408?text=Hola%20quiero%20unirme%20al%20piloto%20CupoYa%20en%20Ocaña";

const FORM_IFRAME_SRC =
  "https://forms.office.com/Pages/ResponsePage.aspx?id=8F_sOLltgEqzVLuE01xjtMuyS05S27NNt7sHSLTJG1FUODNVRjBGWlk4RFVXMzVFRDQxTTBURFlZNC4u&embed=true";

export default function Home() {
  return (
    <main className="min-h-screen px-4 py-10 flex items-center justify-center">
      <div className="w-full max-w-6xl space-y-10">
        {/* Header */}
        <header className="space-y-4">
          {/* Fila mobile: botón arriba a la derecha */}
          <div className="flex justify-end sm:hidden">
            <a
              href={WHATSAPP_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="
                rounded-full px-6 py-3 font-semibold text-navy
                bg-gradient-to-r from-verde-cupo via-cian-radar to-azul-nexo
                hover:brightness-110 transition
                shadow-[0_0_26px_rgba(68,221,105,0.28)]
                border border-white/10
              "
            >
              Contáctenos
            </a>
          </div>

          {/* Contenido: título + subtítulo */}
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight">
                Zona{" "}
                <span className="bg-gradient-to-r from-verde-cupo via-cian-radar to-azul-nexo bg-clip-text text-transparent">
                  CupoYa
                </span>{" "}
                <span className="text-foreground">• Ocaña</span>
              </h1>
              <p className="mt-1 text-muted-foreground text-sm">
                Iniciativa técnologica para Conductores y Dueños de Parqueaderos
              </p>
            </div>

            {/* Botón desktop (a la derecha) */}
            <a
              href={WHATSAPP_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="
                hidden sm:inline-flex
                rounded-full px-6 py-3 font-semibold text-navy
                bg-gradient-to-r from-verde-cupo via-cian-radar to-azul-nexo
                hover:brightness-110 transition
                shadow-[0_0_26px_rgba(68,221,105,0.28)]
                border border-white/10
              "
            >
              Contáctenos
            </a>
          </div>
        </header>

        {/* Hero */}
        <section className="rounded-3xl border border-white/10 bg-white/5 p-8 shadow-glow">
          <h2 className="text-4xl font-bold tracking-tight text-ice">
            Parquear en Ocaña no debería ser una lotería.
          </h2>

          <p className="mt-4 text-ice/70 max-w-3xl leading-relaxed">
            ¿Cansado de dar vueltas, perder tiempo y terminar parqueando “donde se pueda”?{" "}
            <span className="bg-gradient-to-r from-verde-cupo to-azul-nexo bg-clip-text text-transparent">
                <b>CupoYa</b>
            </span> nace para que encuentres parqueadero con claridad y confianza:
            menos vueltas, menos estrés y más control.
            <br />
            <span className="block mt-3">
              Y si administras un parqueadero, {" "}
            <span className="bg-gradient-to-r from-verde-cupo to-azul-nexo bg-clip-text text-transparent">
                <b>CajaCero</b>
            </span>  te ayuda a convertir el caos en operación: ocupación más alta, orden en entradas/salidas y una experiencia que hace que los clientes vuelvan.
            </span>
          </p>
        </section>

        {/* Beneficios */}
        <section id="beneficios" className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* CupoYa Card */}
          <div className="rounded-3xl border border-white/10 bg-white/5 p-8">
            <div className="flex flex-col sm:flex-row sm:items-start gap-5">
              {/* Logo a la izquierda (TODO el bloque) */}
              <div className="shrink-0 flex sm:block justify-center">
                <div className="h-35 w-35 sm:h-35 sm:w-35 rounded-2xl border border-white/10 bg-white/5 p-3 sm:p-4 flex items-center justify-center">
                  <Image
                    src="/brand/cupoya.png"
                    alt="CupoYa"
                    width={100}
                    height={100}
                    className="object-contain"
                    priority
                  />
                </div>
              </div>

              <div className="min-w-0">
                <h3 className="text-xl font-semibold text-ice">
                  Aplicación para Conductores
                </h3>

                <p className="mt-3 text-ice/70 leading-relaxed">
                  Dar vueltas para parquear no es “normal”: es tiempo perdido, gasolina que se va y estrés que te daña el día.
                  {" "}<span className="bg-gradient-to-r from-verde-cupo to-azul-nexo bg-clip-text text-transparent">
                      <b>CupoYa</b>
                  </span>{" "}
                  te ayuda a encontrar opciones con más claridad para que llegues más rápido,
                  con menos incertidumbre y sin improvisar.
                </p>

                <ul className="mt-4 space-y-3 text-ice/70">
                  <li>
                    <span className="text-ice font-semibold">• Se acabó el “a ver si aparece”:</span>{" "}
                    menos vueltas y decisiones más rápidas.
                  </li>
                  <li>
                    <span className="text-ice font-semibold">• Menos riesgo y más tranquilidad:</span>{" "}
                    evita zonas incómodas y reduce el estrés de buscar a última hora.
                  </li>
                  <li>
                    <span className="text-ice font-semibold">• Pensado para tu rutina:</span>{" "}
                    por horas o mensual (según disponibilidad) para que pares de improvisar.
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* CajaCero Card */}
          <div className="rounded-3xl border border-white/10 bg-white/5 p-8">
            <div className="flex flex-col sm:flex-row sm:items-start gap-5">
              {/* Logo a la izquierda (TODO el bloque) */}
              <div className="shrink-0 flex sm:block justify-center">
                <div className="h-35 w-35 sm:h-35 sm:w-35 rounded-2xl border border-white/10 bg-white/5 p-3 sm:p-4 flex items-center justify-center">
                  <Image
                    src="/brand/cajacero.png"
                    alt="CajaCero"
                    width={100}
                    height={100}
                    className="object-contain"
                  />
                </div>
              </div>

              <div className="min-w-0">
                <h3 className="text-xl font-semibold text-ice">
                  Aplicación para Parqueaderos
                </h3>

                <p className="mt-3 text-ice/70 leading-relaxed">
                  Cupos vacíos en horas clave, desorden en la entrada/salida y clientes molestos…
                  eso no es “parte del negocio”, es dinero escapándose todos los días.
                  {" "}<span className="bg-gradient-to-r from-verde-cupo to-azul-nexo bg-clip-text text-transparent">
                      <b>CajaCero</b>
                  </span>{" "} te ayuda a ordenar la operación y a convertir capacidad en ingresos reales.
                </p>

                <ul className="mt-4 space-y-3 text-ice/70">
                  <li>
                    <span className="text-ice font-semibold">• Más ocupación, menos huecos:</span>{" "}
                    aprovecha mejor tu capacidad y reduce tiempos muertos.
                  </li>
                  <li>
                    <span className="text-ice font-semibold">• Operación más clara:</span>{" "}
                    menos confusión, menos fricción y mejor control.
                  </li>
                  <li>
                    <span className="text-ice font-semibold">• Mejor experiencia = más retorno:</span>{" "}
                    si el servicio es ágil, los clientes vuelven y recomiendan.
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>


        {/* Waitlist */}
        <section id="waitlist" className="rounded-3xl border border-white/10 bg-white/5 p-8 shadow-glow">
          <h3 className="text-2xl font-semibold text-ice">Lista de espera</h3>
          <p className="mt-2 text-ice/70">
            Déjanos tus datos y te contactamos para habilitar una Prueba de Valor.
          </p>

          <div className="mt-6 rounded-2xl overflow-hidden border border-white/10 bg-navy/50">
            <div style={{ position: "relative", width: "100%", height: 820 }}>
              <iframe
                src={FORM_IFRAME_SRC}
                style={{ position: "absolute", inset: 0, width: "100%", height: "100%", border: 0 }}
                allowFullScreen
                title="Formulario de lista de espera"
              />
            </div>
          </div>

          <p className="mt-3 text-xs text-ice/60">
            Tus datos se usan solo para contactarte sobre el piloto en Ocaña.
          </p>
        </section>

        {/* Footer */}
        <footer className="flex flex-wrap items-center justify-between gap-4 text-ice/60 text-sm">
          <span>© {new Date().getFullYear()} CupoYa • Iniciativa Técnologica Ocaña</span>
          <div className="flex items-center gap-2">
            <span className="text-ice/60">Operado por</span>
            <Image src="/brand/nexohub.png" alt="NexoHub" width={35} height={35} />
          </div>
        </footer>
      </div>
    </main>
  );
}
