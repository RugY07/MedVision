import { motion } from "framer-motion";
import { Button } from "./ui/button";
import { Rocket } from "lucide-react";

const CallToAction = () => {
  return (
    <section className="py-20 px-6 relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-card/50 to-background" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_hsl(188_100%_50%_/_0.15),_transparent_60%)]" />

      <div className="container mx-auto relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl mx-auto text-center space-y-8"
        >
          {/* Animated background card */}
          <div className="relative p-12 rounded-3xl glass-morphism holographic-border">
            {/* Decorative elements */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2">
              <div className="w-16 h-16 rounded-full bg-medical-cyan/20 blur-xl animate-pulse-glow" />
            </div>

            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              whileInView={{ scale: 1, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="space-y-6"
            >
              <h2 className="text-4xl lg:text-5xl font-bold">
                <span className="text-foreground/90">Ready to Transform</span>
                <br />
                <span className="glow-text">Medical Diagnostics?</span>
              </h2>

              <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                Join leading medical institutions using MedVision AI for faster, more accurate 
                diagnoses with cutting-edge technology.
              </p>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.4 }}
                className="pt-4"
              >
                <Button 
                  size="lg" 
                  className="group relative overflow-hidden text-lg px-8 py-6"
                  onClick={() => {
                    document.getElementById('upload-section')?.scrollIntoView({ 
                      behavior: 'smooth' 
                    });
                  }}
                >
                  <span className="relative z-10 flex items-center gap-2">
                    <Rocket className="w-6 h-6" />
                    Launch MedVision AI
                  </span>
                  <div className="absolute inset-0 bg-gradient-to-r from-medical-cyan to-medical-purple opacity-0 group-hover:opacity-100 transition-opacity" />
                </Button>
              </motion.div>
            </motion.div>

            {/* Floating particles */}
            {[...Array(6)].map((_, i) => (
              <motion.div
                key={i}
                className="absolute w-2 h-2 rounded-full bg-medical-cyan/30"
                style={{
                  top: `${Math.random() * 100}%`,
                  left: `${Math.random() * 100}%`,
                }}
                animate={{
                  y: [0, -20, 0],
                  opacity: [0.3, 0.8, 0.3],
                }}
                transition={{
                  duration: 3,
                  delay: i * 0.5,
                  repeat: Infinity,
                  ease: 'easeInOut',
                }}
              />
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default CallToAction;
