import { motion } from "framer-motion";
import { Play } from "lucide-react";

const DemoSection = () => {
  return (
    <section id="demo" className="py-20 px-6">
      <div className="container mx-auto max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold mb-4">
            <span className="glow-text">See MedVision AI in Action</span>
          </h2>
          <p className="text-muted-foreground text-lg">
            Watch how our AI revolutionizes medical diagnostics
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="relative rounded-2xl overflow-hidden glass-morphism holographic-border"
        >
          <div className="absolute inset-0 bg-gradient-to-br from-medical-cyan/10 to-medical-purple/10" />
          
          <video
            controls
            className="w-full aspect-video relative z-10"
            poster="/placeholder.svg"
          >
            <source src="/demo-video.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>

          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none">
            <div className="w-20 h-20 rounded-full bg-medical-cyan/20 backdrop-blur-sm flex items-center justify-center">
              <Play className="w-10 h-10 text-medical-cyan" />
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default DemoSection;
