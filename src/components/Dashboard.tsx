import { motion } from "framer-motion";
import { Activity, Clock, AlertTriangle, CheckCircle } from "lucide-react";
import { Card } from "./ui/card";

const stats = [
  {
    icon: Activity,
    label: "Total Scans",
    value: "1,247",
    color: "text-medical-cyan"
  },
  {
    icon: Clock,
    label: "Pending Analysis",
    value: "23",
    color: "text-warning-amber"
  },
  {
    icon: AlertTriangle,
    label: "Critical Cases",
    value: "3",
    color: "text-destructive"
  },
  {
    icon: CheckCircle,
    label: "Completed Today",
    value: "89",
    color: "text-medical-green"
  }
];

const Dashboard = () => {
  return (
    <section className="py-12 px-6 relative">
      <div className="container mx-auto max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="grid grid-cols-2 lg:grid-cols-4 gap-4"
        >
          {stats.map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className="p-6 glass-morphism holographic-border hover:scale-105 transition-all">
                <div className="flex items-center justify-between mb-3">
                  <stat.icon className={`w-5 h-5 ${stat.color}`} />
                </div>
                <div className={`text-3xl font-bold mb-1 ${stat.color}`}>
                  {stat.value}
                </div>
                <div className="text-sm text-muted-foreground">
                  {stat.label}
                </div>
              </Card>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
};

export default Dashboard;
