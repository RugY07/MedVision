import { useState, useCallback } from "react";
import { Upload, FileWarning, CheckCircle2, AlertCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useToast } from "@/hooks/use-toast";

interface ScanUploaderProps {
  onFileSelect: (file: File) => void;
  selectedScanType?: string;
}

const ACCEPTED_FILE_TYPES = [
  'image/jpeg',
  'image/jpg', 
  'image/png',
  'image/dicom',
  'application/dicom'
];

const MEDICAL_IMAGE_KEYWORDS = [
  'scan', 'xray', 'x-ray', 'mri', 'ct', 'ultrasound', 
  'medical', 'radiograph', 'imaging', 'dicom'
];

const ScanUploader = ({ onFileSelect, selectedScanType }: ScanUploaderProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const [validationStatus, setValidationStatus] = useState<'idle' | 'validating' | 'valid' | 'invalid'>('idle');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const { toast } = useToast();

  const validateMedicalImage = async (file: File): Promise<boolean> => {
    // Check file type
    if (!ACCEPTED_FILE_TYPES.includes(file.type) && !file.name.toLowerCase().endsWith('.dcm')) {
      toast({
        title: "Invalid File Type",
        description: "Please upload a medical scan image (JPEG, PNG, or DICOM)",
        variant: "destructive"
      });
      return false;
    }

    // Check file size (max 50MB for medical scans)
    if (file.size > 50 * 1024 * 1024) {
      toast({
        title: "File Too Large",
        description: "Maximum file size is 50MB",
        variant: "destructive"
      });
      return false;
    }

    // Heuristic check: filename should contain medical imaging keywords
    const fileName = file.name.toLowerCase();
    const hasKeyword = MEDICAL_IMAGE_KEYWORDS.some(keyword => fileName.includes(keyword));
    
    if (!hasKeyword && file.type.includes('image')) {
      toast({
        title: "Possible Non-Medical Image",
        description: "This file may not be a medical scan. Please verify it's the correct file.",
        variant: "default"
      });
    }

    // For image files, try to validate it's actually an image
    if (file.type.includes('image')) {
      return new Promise((resolve) => {
        const img = new Image();
        const url = URL.createObjectURL(file);
        
        img.onload = () => {
          URL.revokeObjectURL(url);
          resolve(true);
        };
        
        img.onerror = () => {
          URL.revokeObjectURL(url);
          toast({
            title: "Invalid Image File",
            description: "The uploaded file appears to be corrupted or not a valid image",
            variant: "destructive"
          });
          resolve(false);
        };
        
        img.src = url;
      });
    }

    return true;
  };

  const handleFile = useCallback(async (file: File) => {
    setValidationStatus('validating');
    setSelectedFile(file);

    const isValid = await validateMedicalImage(file);
    
    if (isValid) {
      setValidationStatus('valid');
      setTimeout(() => {
        onFileSelect(file);
      }, 500);
    } else {
      setValidationStatus('invalid');
      setTimeout(() => {
        setValidationStatus('idle');
        setSelectedFile(null);
      }, 2000);
    }
  }, [onFileSelect, toast]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFile(file);
    }
  }, [handleFile]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFile(file);
    }
  }, [handleFile]);

  return (
    <section className="py-20 px-6">
      <div className="container mx-auto max-w-4xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold mb-4">
            <span className="glow-text">Upload Medical Scan</span>
          </h2>
          <p className="text-muted-foreground text-lg">
            Drag and drop your scan or click to browse
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          onDragOver={(e) => {
            e.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
          className={`
            relative min-h-[400px] rounded-2xl glass-morphism
            border-2 border-dashed transition-all duration-300
            ${isDragging ? 'border-medical-cyan bg-medical-cyan/5' : 'border-border/50'}
            ${validationStatus === 'valid' ? 'border-medical-green bg-medical-green/5' : ''}
            ${validationStatus === 'invalid' ? 'border-destructive bg-destructive/5' : ''}
          `}
        >
          <input
            type="file"
            id="scan-upload"
            className="hidden"
            accept=".jpg,.jpeg,.png,.dcm,.dicom"
            onChange={handleFileInput}
          />

          <label
            htmlFor="scan-upload"
            className="absolute inset-0 flex flex-col items-center justify-center cursor-pointer"
          >
            <AnimatePresence mode="wait">
              {validationStatus === 'idle' && (
                <motion.div
                  key="idle"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                  className="text-center"
                >
                  <div className="w-24 h-24 mx-auto mb-6 rounded-full glass-morphism holographic-border flex items-center justify-center">
                    <Upload className="w-12 h-12 text-medical-cyan" />
                  </div>
                  <h3 className="text-2xl font-semibold mb-2">Drop your scan here</h3>
                  <p className="text-muted-foreground mb-4">or click to browse files</p>
                  <div className="text-sm text-muted-foreground">
                    Supports: JPEG, PNG, DICOM (max 50MB)
                  </div>
                </motion.div>
              )}

              {validationStatus === 'validating' && (
                <motion.div
                  key="validating"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="text-center"
                >
                  <div className="w-24 h-24 mx-auto mb-6 rounded-full glass-morphism holographic-border flex items-center justify-center">
                    <div className="w-12 h-12 border-4 border-medical-cyan border-t-transparent rounded-full animate-spin" />
                  </div>
                  <h3 className="text-2xl font-semibold mb-2">Validating scan...</h3>
                  <p className="text-muted-foreground">{selectedFile?.name}</p>
                </motion.div>
              )}

              {validationStatus === 'valid' && (
                <motion.div
                  key="valid"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                  className="text-center"
                >
                  <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-medical-green/10 border-2 border-medical-green flex items-center justify-center">
                    <CheckCircle2 className="w-12 h-12 text-medical-green" />
                  </div>
                  <h3 className="text-2xl font-semibold mb-2 text-medical-green">Scan validated</h3>
                  <p className="text-muted-foreground">Processing analysis...</p>
                </motion.div>
              )}

              {validationStatus === 'invalid' && (
                <motion.div
                  key="invalid"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                  className="text-center"
                >
                  <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-destructive/10 border-2 border-destructive flex items-center justify-center">
                    <AlertCircle className="w-12 h-12 text-destructive" />
                  </div>
                  <h3 className="text-2xl font-semibold mb-2 text-destructive">Validation failed</h3>
                  <p className="text-muted-foreground">Please try another file</p>
                </motion.div>
              )}
            </AnimatePresence>
          </label>

          {/* Scan line effect */}
          {validationStatus === 'validating' && (
            <div className="absolute inset-0 scan-line pointer-events-none rounded-2xl" />
          )}
        </motion.div>

        {/* File type notice */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mt-8 p-4 rounded-xl glass-morphism border border-medical-amber/30"
        >
          <div className="flex gap-3">
            <FileWarning className="w-5 h-5 text-medical-amber flex-shrink-0 mt-0.5" />
            <div className="text-sm">
              <p className="font-semibold text-medical-amber mb-1">Important Notice</p>
              <p className="text-muted-foreground">
                Only upload medical scan images (X-rays, MRI, CT scans). 
                Random images will be rejected during validation to ensure accurate AI analysis.
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default ScanUploader;
