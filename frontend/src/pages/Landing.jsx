import React from 'react';
import TopNavBar from '../components/Landing/TopNavBar';
import HeroSection from '../components/Landing/HeroSection';
import FeatureSection from '../components/Landing/FeatureSection';
import TestimonialsSection from '../components/Landing/TestimonialsSection';
import CTASection from '../components/Landing/CTASection';
import Footer from '../components/Landing/Footer';

function Landing() {
  return (
    <div className='dark'>
    <div className="relative flex min-h-screen w-full flex-col bg-background-light dark:bg-background-dark group/design-root overflow-x-hidden">
      <div className="layout-container flex h-full grow flex-col">
        <div className="px-4 sm:px-10 md:px-20 lg:px-40 flex flex-1 justify-center py-5">
          <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
            <TopNavBar />
            
            <main className="flex flex-col gap-12 sm:gap-16 md:gap-20">
              <HeroSection />
              <FeatureSection />
              <TestimonialsSection />
              <CTASection />
            </main>
            
            <Footer />
          </div>
        </div>
      </div>
    </div>
    </div>
  );
}

export default Landing;