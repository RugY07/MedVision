import Navigation from "@/components/Navigation";
import Hero from "@/components/Hero";
import Features from "@/components/Features";
import HolographicDiagnostics from "@/components/HolographicDiagnostics";
import CallToAction from "@/components/CallToAction";
import Footer from "@/components/Footer";
import Dashboard from "@/components/Dashboard";
import ScanTypeSelector from "@/components/ScanTypeSelector";
import DemoSection from "@/components/DemoSection";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <Hero />
      <Dashboard />
      <section id="scan-types" className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <ScanTypeSelector />
        </div>
      </section>
      <Features />
      <HolographicDiagnostics />
      <DemoSection />
      <CallToAction />
      <Footer />
    </div>
  );
};

export default Index;
