import { motion } from "framer-motion";
import { Brain, Zap, Shield, Eye } from "lucide-react";
import { Card } from "./ui/card";

const features = [
  {
    icon: Brain,
    title: "AI-Powered Diagnostics",
    description: "Advanced neural networks analyze medical scans with 99.2% accuracy",
    color: "text-medical-cyan"
  },
  {
    icon: Eye,
    title: "Holographic Visualization",
    description: "3D organ models and AR projection for immersive analysis",
    color: "text-medical-purple"
  },
  {
    icon: Shield,
    title: "HIPAA Compliant",
    description: "Enterprise-grade security with zero PHI storage",
    color: "text-medical-green"
  },
  {
    icon: Zap,
    title: "Real-time Processing",
    description: "Sub-second inference with WebGPU acceleration",
    color: "text-medical-cyan"
  }
];

const Features = () => {
  return (
    <section id="features" className="py-20 px-6 relative">
      {/* Background effects */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-background/50 to-background pointer-events-none" />
      
      <div className="container mx-auto max-w-7xl relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold mb-4">
            <span className="glow-text">Advanced Features</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Cutting-edge technology meets medical expertise in our comprehensive diagnostic platform
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className="p-6 glass-morphism holographic-border h-full hover:scale-105 transition-all duration-300 group">
                <div className={`w-14 h-14 rounded-xl glass-morphism holographic-border flex items-center justify-center mb-4 group-hover:scale-110 transition-transform ${feature.color}`}>
                  <feature.icon className="w-7 h-7" />
                </div>
                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                <p className="text-muted-foreground">{feature.description}</p>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Stats section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-20 grid grid-cols-2 lg:grid-cols-4 gap-8"
        >
          {[
            { label: "Scans Analyzed", value: "2M+", color: "text-medical-cyan" },
            { label: "Accuracy Rate", value: "98.7%", color: "text-medical-green" },
            { label: "Active Clinicians", value: "15K+", color: "text-medical-purple" },
            { label: "Countries", value: "80+", color: "text-medical-cyan" }
          ].map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="text-center p-6 rounded-xl glass-morphism holographic-border"
            >
              <div className={`text-4xl lg:text-5xl font-bold mb-2 ${stat.color} glow-text`}>
                {stat.value}
              </div>
              <div className="text-sm text-muted-foreground">{stat.label}</div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default Features;
