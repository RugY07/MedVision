import { motion } from "framer-motion";
import { Brain, Heart, Wind, Bone } from "lucide-react";
import { Card } from "./ui/card";
import { useNavigate } from "react-router-dom";

interface ScanTypeSelectorProps {
  selectedType?: string;
  onSelectType?: (type: string) => void;
}

const scanTypes = [
  {
    id: "Brain",
    label: "Brain",
    icon: Brain,
    color: "text-purple-400",
    description: "Neural, MRI, CT scans"
  },
  {
    id: "Cardiac",
    label: "Heart",
    icon: Heart,
    color: "text-red-400",
    description: "Cardiac imaging"
  },
  {
    id: "Chest/Lungs",
    label: "Lungs",
    icon: Wind,
    color: "text-cyan-400",
    description: "Chest X-rays, CT scans"
  },
  {
    id: "Bone",
    label: "Bones",
    icon: Bone,
    color: "text-green-400",
    description: "Skeletal imaging"
  }
];

const ScanTypeSelector = ({ selectedType, onSelectType }: ScanTypeSelectorProps) => {
  const navigate = useNavigate();

  const handleSelectType = (typeId: string) => {
    if (onSelectType) {
      onSelectType(typeId);
    } else {
      // Navigate to dedicated scan page
      switch (typeId) {
        case 'Brain':
          navigate('/brain-scan');
          break;
        case 'Cardiac':
          navigate('/cardiac-scan');
          break;
        case 'Chest/Lungs':
          navigate('/chest-scan');
          break;
        case 'Bone':
          navigate('/bone-scan');
          break;
      }
    }
  };

  return (
    <div id="scan-types" className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h2 className="text-3xl font-bold mb-2">
          <span className="glow-text">Select Scan Type</span>
        </h2>
        <p className="text-muted-foreground">
          Choose the type of medical scan you want to analyze
        </p>
      </motion.div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {scanTypes.map((type, index) => (
          <motion.div
            key={type.id}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card
              onClick={() => handleSelectType(type.id)}
              className={`
                p-6 glass-morphism cursor-pointer transition-all duration-300
                ${selectedType === type.id 
                  ? 'holographic-border scale-105' 
                  : 'hover:scale-105 hover:holographic-border'
                }
              `}
            >
              <div className="text-center space-y-3">
                <div className={`w-16 h-16 mx-auto rounded-xl glass-morphism flex items-center justify-center ${type.color}`}>
                  <type.icon className="w-8 h-8" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">{type.label}</h3>
                  <p className="text-xs text-muted-foreground">{type.description}</p>
                </div>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default ScanTypeSelector;
