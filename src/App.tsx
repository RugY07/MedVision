import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import BrainScan from "./pages/BrainScan";
import CardiacScan from "./pages/CardiacScan";
import ChestScan from "./pages/ChestScan";
import BoneScan from "./pages/BoneScan";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/brain-scan" element={<BrainScan />} />
          <Route path="/cardiac-scan" element={<CardiacScan />} />
          <Route path="/chest-scan" element={<ChestScan />} />
          <Route path="/bone-scan" element={<BoneScan />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
