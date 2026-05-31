import { motion } from "framer-motion";
import { Layers, Scan, Vibrate, Eye } from "lucide-react";
import { Card } from "./ui/card";

const capabilities = [
  {
    icon: Eye,
    title: "WebXR-based AR projection",
    description: "Project scans in augmented reality for immersive viewing"
  },
  {
    icon: Layers,
    title: "Real-time 3D organ modeling",
    description: "Dynamic 3D reconstruction from 2D scan data"
  },
  {
    icon: Vibrate,
    title: "Haptic feedback integration",
    description: "Tactile alerts for critical findings and anomalies"
  }
];

const scanTypes = [
  { name: "Cardiac", color: "text-red-400" },
  { name: "Neural", color: "text-purple-400" },
  { name: "Pulmonary", color: "text-cyan-400" }
];

const HolographicDiagnostics = () => {
  return (
    <section id="technology" className="py-20 px-6 relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-background/95 to-background" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_hsl(188_100%_50%_/_0.1),_transparent_70%)]" />

      <div className="container mx-auto relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left: 3D Visual */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="relative"
          >
            <div className="aspect-square relative rounded-2xl overflow-hidden glass-morphism holographic-border animate-float">
              <div className="absolute inset-0 flex items-center justify-center">
                <Scan className="w-32 h-32 text-medical-cyan animate-pulse-glow" />
              </div>
              {/* Animated rings */}
              <div className="absolute inset-0 flex items-center justify-center">
                {[0, 1, 2].map((i) => (
                  <motion.div
                    key={i}
                    className="absolute rounded-full border border-medical-cyan/30"
                    initial={{ width: 0, height: 0, opacity: 0 }}
                    animate={{
                      width: ['0%', '100%'],
                      height: ['0%', '100%'],
                      opacity: [0.5, 0],
                    }}
                    transition={{
                      duration: 3,
                      delay: i * 1,
                      repeat: Infinity,
                      ease: 'easeOut',
                    }}
                  />
                ))}
              </div>
            </div>
            {/* Glow effect */}
            <div className="absolute -inset-4 bg-gradient-to-r from-medical-cyan/20 to-medical-purple/20 blur-3xl -z-10 animate-pulse-glow" />
          </motion.div>

          {/* Right: Content */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="space-y-8"
          >
            <div className="space-y-4">
              <h2 className="text-4xl lg:text-5xl font-bold">
                <span className="glow-text">Holographic</span>
                <br />
                <span className="text-foreground/90">Diagnostics</span>
              </h2>
              <p className="text-xl text-muted-foreground">
                Experience medical imaging like never before with our 3D holographic interfaces, 
                AR projection capabilities, and immersive organ visualization.
              </p>
            </div>

            {/* Capabilities */}
            <div className="space-y-4">
              {capabilities.map((capability, index) => (
                <motion.div
                  key={capability.title}
                  initial={{ opacity: 0, x: 20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Card className="p-4 glass-morphism hover:holographic-border transition-all duration-300">
                    <div className="flex items-start gap-4">
                      <div className="p-2 rounded-lg bg-medical-cyan/10">
                        <capability.icon className="w-6 h-6 text-medical-cyan" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-lg mb-1">{capability.title}</h3>
                        <p className="text-muted-foreground text-sm">{capability.description}</p>
                      </div>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </div>

            {/* Scan Types */}
            <div className="flex flex-wrap gap-3 pt-4">
              {scanTypes.map((type, index) => (
                <motion.div
                  key={type.name}
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="px-6 py-3 rounded-full glass-morphism holographic-border"
                >
                  <span className={`font-semibold ${type.color}`}>{type.name}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default HolographicDiagnostics;
