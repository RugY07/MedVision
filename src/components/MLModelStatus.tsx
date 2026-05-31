"""
ML Model Status Component
Shows the status of trained ML models for each scan type
"""

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { CheckCircle, XCircle, Clock, RefreshCw } from 'lucide-react';
import { motion } from 'framer-motion';

interface ModelStatus {
  scanType: string;
  loaded: boolean;
  classes: string[];
  modelPath: string;
  lastUpdated?: string;
  accuracy?: number;
  f1Score?: number;
}

interface MLModelStatusProps {
  className?: string;
}

const MLModelStatus: React.FC<MLModelStatusProps> = ({ className }) => {
  const [modelStatuses, setModelStatuses] = useState<ModelStatus[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchModelStatus = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Try to fetch from ML model server first
      const ML_SERVER_URL = import.meta.env.VITE_ML_SERVER_URL || 'http://localhost:8000';
      
      const response = await fetch(`${ML_SERVER_URL}/models/status`);
      
      if (response.ok) {
        const data = await response.json();
        const statuses: ModelStatus[] = Object.entries(data).map(([scanType, info]: [string, any]) => ({
          scanType,
          loaded: info.loaded,
          classes: info.classes,
          modelPath: info.model_path,
          lastUpdated: info.last_updated
        }));
        setModelStatuses(statuses);
      } else {
        // Fallback: check if models are available locally
        const scanTypes = ['brain', 'cardiac', 'chest', 'bone'];
        const statuses: ModelStatus[] = scanTypes.map(scanType => ({
          scanType,
          loaded: false,
          classes: getDefaultClasses(scanType),
          modelPath: `models/${scanType}/${scanType}_best_model.pth`
        }));
        setModelStatuses(statuses);
      }
    } catch (err) {
      console.error('Error fetching model status:', err);
      setError('Unable to connect to ML model server');
      
      // Set default statuses
      const scanTypes = ['brain', 'cardiac', 'chest', 'bone'];
      const statuses: ModelStatus[] = scanTypes.map(scanType => ({
        scanType,
        loaded: false,
        classes: getDefaultClasses(scanType),
        modelPath: `models/${scanType}/${scanType}_best_model.pth`
      }));
      setModelStatuses(statuses);
    } finally {
      setIsLoading(false);
    }
  };

  const getDefaultClasses = (scanType: string): string[] => {
    const classMapping = {
      brain: ['normal', 'tumor', 'stroke', 'hemorrhage', 'atrophy'],
      cardiac: ['normal', 'cardiomyopathy', 'valvular_disease', 'coronary_disease', 'arrhythmia'],
      chest: ['normal', 'pneumonia', 'covid', 'tuberculosis', 'lung_cancer', 'pneumothorax'],
      bone: ['normal', 'fracture', 'osteoporosis', 'arthritis', 'tumor']
    };
    return classMapping[scanType as keyof typeof classMapping] || [];
  };

  useEffect(() => {
    fetchModelStatus();
  }, []);

  const getStatusIcon = (loaded: boolean) => {
    if (loaded) {
      return <CheckCircle className="h-5 w-5 text-green-500" />;
    }
    return <XCircle className="h-5 w-5 text-red-500" />;
  };

  const getStatusBadge = (loaded: boolean) => {
    if (loaded) {
      return <Badge variant="default" className="bg-green-500">Ready</Badge>;
    }
    return <Badge variant="destructive">Not Available</Badge>;
  };

  if (isLoading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="h-5 w-5" />
            ML Model Status
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <RefreshCw className="h-6 w-6 animate-spin" />
            <span className="ml-2">Checking model status...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Clock className="h-5 w-5" />
            ML Model Status
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={fetchModelStatus}
            disabled={isLoading}
          >
            <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {error && (
          <Alert>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {modelStatuses.map((status, index) => (
            <motion.div
              key={status.scanType}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className="border-l-4 border-l-blue-500">
                <CardHeader className="pb-2">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg capitalize">
                      {status.scanType} Scans
                    </CardTitle>
                    {getStatusIcon(status.loaded)}
                  </div>
                </CardHeader>
                <CardContent className="pt-0">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Status:</span>
                      {getStatusBadge(status.loaded)}
                    </div>
                    
                    <div>
                      <span className="text-sm text-gray-600">Classes:</span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {status.classes.map((className) => (
                          <Badge key={className} variant="outline" className="text-xs">
                            {className.replace('_', ' ')}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    {status.loaded && (
                      <div className="text-xs text-gray-500">
                        Model Path: {status.modelPath}
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
          <h4 className="font-semibold text-blue-900 mb-2">Model Information</h4>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Trained models provide specialized analysis for each scan type</li>
            <li>• Models use EfficientNet-B4 architecture with medical-specific preprocessing</li>
            <li>• Each model is trained on domain-specific datasets</li>
            <li>• Fallback to general AI models when custom models are unavailable</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  );
};

export default MLModelStatus;
