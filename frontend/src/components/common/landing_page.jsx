/*
AMEP - Single-file React App (App.jsx)

Instructions:
1. Create a Vite React project (or add to your existing React app).
   npx create-vite@latest amep --template react
2. Install Tailwind CSS (recommended):
   Follow Tailwind docs for Vite + React: https://tailwindcss.com/docs/guides/vite
   Or, for a quick demo, you can include the Tailwind CDN in public/index.html (not recommended for production).
3. Add the Material Symbols and Inter font links to public/index.html <head> (same links used in your HTML).
4. Replace src/App.jsx with the content of this file. Ensure src/index.css imports Tailwind base/utilities.

This file contains all page sections as self-contained React components:
- Navbar
- HeroSection
- FeaturesSection
- ReviewsSection
- FAQSection
- Footer

You can split components into separate files later; this single-file layout is convenient for quick conversion and preview.
*/

import React from "react";

function Navbar() {
  return (
    <header className="flex items-center justify-between whitespace-nowrap py-6">
      <div className="flex items-center gap-4 text-white">
        <div className="h-8 w-8 text-primary">
          <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
            <path d="M42.4379 44C42.4379 44 36.0744 33.9038 41.1692 24C46.8624 12.9336 42.2078 4 42.2078 4L7.01134 4C7.01134 4 11.6577 12.932 5.96912 23.9969C0.876273 33.9029 7.27094 44 7.27094 44L42.4379 44Z" fill="currentColor"></path>
          </svg>
        </div>
        <h2 className="text-xl font-bold leading-tight tracking-[-0.015em]">AMEP</h2>
      </div>

      <nav className="hidden items-center gap-8 md:flex">
        <a className="text-sm font-medium text-gray-300 hover:text-white" href="#">Courses</a>
        <a className="text-sm font-medium text-gray-300 hover:text-white" href="#features">Features</a>
        <a className="text-sm font-medium text-gray-300 hover:text-white" href="#reviews">Testimonials</a>
        <a className="text-sm font-medium text-gray-300 hover:text-white" href="#faq">FAQ</a>
      </nav>

      <div className="flex items-center gap-2">
        <button className="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-transparent text-white text-sm font-medium leading-normal hover:bg-white/10">
          <span className="truncate">Login</span>
        </button>
        <button className="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold leading-normal hover:bg-blue-500 transition-colors">
          <span className="truncate">Register</span>
        </button>
      </div>
    </header>
  );
}

function HeroSection() {
  return (
    <section className="relative py-20 text-center sm:py-28 md:py-32 lg:py-40">
      <div className="absolute inset-0 hero-gradient" />
      <div className="relative z-10 mx-auto max-w-3xl">
        <div className="flex flex-col items-center gap-6">
          <h1 className="text-4xl font-black leading-tight tracking-tighter text-white sm:text-5xl md:text-6xl">Unlock Your Future with AMEP</h1>
          <p className="text-base font-normal leading-normal text-gray-300 md:text-lg">Discover interactive courses, expert tutors, and flexible learning paths tailored to your goals.</p>
          <button className="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-6 bg-primary text-white text-base font-bold leading-normal tracking-wide shadow-lg shadow-blue-500/30 transition-transform hover:scale-105">
            <span className="truncate">Get Started</span>
          </button>
        </div>
      </div>
    </section>
  );
}

function FeatureCard({ icon, title, desc, accent }) {
  return (
    <div className="flex flex-col gap-4 rounded-xl border border-white/10 p-6 text-center shadow-lg transition-all hover:border-primary/50 hover:shadow-primary/20 glassmorphism">
      <div className={`mx-auto flex h-12 w-12 items-center justify-center rounded-lg ${accent}`}>
        <span className="material-symbols-outlined text-3xl">{icon}</span>
      </div>
      <div className="flex flex-col gap-1">
        <h3 className="text-lg font-bold text-white">{title}</h3>
        <p className="text-sm text-gray-300">{desc}</p>
      </div>
    </div>
  );
}

function FeaturesSection() {
  return (
    <section id="features" className="py-16 sm:py-24">
      <div className="flex flex-col gap-12">
        <div className="flex flex-col gap-3 text-center">
          <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">Why Choose AMEP?</h2>
          <p className="text-base text-gray-400 sm:text-lg">We provide a cutting-edge platform designed for modern learners.</p>
        </div>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
          <FeatureCard icon="auto_stories" title="Interactive Courses" desc="Engage with dynamic content and hands-on projects." accent="bg-indigo-accent/20 text-indigo-accent" />
          <FeatureCard icon="school" title="Expert Tutors" desc="Learn from the best in the industry with personalized guidance." accent="bg-teal-accent/20 text-teal-accent" />
          <FeatureCard icon="schedule" title="Flexible Learning" desc="Study at your own pace, anytime, anywhere." accent="bg-primary/20 text-primary" />
        </div>
      </div>
    </section>
  );
}

function ReviewCard({ avatar, name, role, text }) {
  return (
    <div className="flex flex-col gap-4 rounded-xl border border-white/10 bg-white/5 p-6">
      <div className="flex items-center gap-4">
        <div className="h-12 w-12 rounded-full bg-cover bg-center" style={{ backgroundImage: `url('${avatar}')` }} aria-hidden />
        <div>
          <p className="font-semibold text-white">{name}</p>
          <p className="text-sm text-gray-400">{role}</p>
        </div>
      </div>
      <div className="flex gap-0.5 text-yellow-400">
        {Array.from({ length: 5 }).map((_, i) => (
          <span key={i} className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>star</span>
        ))}
      </div>
      <p className="text-gray-300">{text}</p>
    </div>
  );
}

function ReviewsSection() {
  return (
    <section id="reviews" className="py-16 sm:py-24">
      <div className="flex flex-col gap-12">
        <div className="flex flex-col gap-3 text-center">
          <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">What Our Students Say</h2>
          <p className="text-base text-gray-400 sm:text-lg">Real stories from learners who transformed their careers with us.</p>
        </div>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          <ReviewCard avatar="https://i.pravatar.cc/100?img=32" name="Jane Doe" role="Software Engineer" text="AMEP transformed my learning experience. The courses are incredibly engaging and the tutors are top-notch!" />
          <ReviewCard avatar="https://i.pravatar.cc/100?img=12" name="John Smith" role="Product Manager" text="A fantastic platform with a modern interface and flexible schedules. Highly recommended for anyone looking to upskill." />
        </div>
      </div>
    </section>
  );
}

function FAQItem({ q, a }) {
  return (
    <details className="group rounded-lg bg-white/5 p-4">
      <summary className="flex cursor-pointer list-none items-center justify-between font-medium text-white">
        {q}
        <span className="transition-transform group-open:rotate-45">
          <span className="material-symbols-outlined">add</span>
        </span>
      </summary>
      <p className="mt-4 text-gray-300">{a}</p>
    </details>
  );
}

function FAQSection() {
  const faqs = [
    {
      q: "What is the cost of a course?",
      a:
        "Course prices vary depending on the subject and duration. We offer both individual course purchases and subscription plans for full access. Please visit our 'Courses' page for detailed pricing information.",
    },
    {
      q: "Are the courses self-paced?",
      a: "Yes, all our courses are designed to be self-paced so you can learn at your own convenience. You will have lifetime access to the course materials after purchase.",
    },
    {
      q: "Do I get a certificate upon completion?",
      a: "Absolutely! Upon successful completion of any course, you will receive a verifiable certificate from AMEP that you can share on your professional networks and resume.",
    },
  ];

  return (
    <section id="faq" className="py-16 sm:py-24">
      <div className="mx-auto max-w-3xl">
        <div className="flex flex-col gap-12">
          <div className="flex flex-col gap-3 text-center">
            <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">Frequently Asked Questions</h2>
            <p className="text-base text-gray-400 sm:text-lg">Find answers to common questions about our platform and courses.</p>
          </div>
          <div className="flex flex-col gap-4">
            {faqs.map((f, i) => (
              <FAQItem key={i} q={f.q} a={f.a} />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="border-t border-white/10 py-12">
      <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
        <div className="col-span-2 md:col-span-1">
          <div className="flex items-center gap-2">
            <div className="h-6 w-6 text-primary">
              <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                <path d="M42.4379 44C42.4379 44 36.0744 33.9038 41.1692 24C46.8624 12.9336 42.2078 4 42.2078 4L7.01134 4C7.01134 4 11.6577 12.932 5.96912 23.9969C0.876273 33.9029 7.27094 44 7.27094 44L42.4379 44Z" fill="currentColor"></path>
              </svg>
            </div>
            <h2 className="text-lg font-bold">AMEP</h2>
          </div>
          <p className="mt-4 text-sm text-gray-400">Empowering the next generation of learners.</p>
        </div>

        <div>
          <h3 className="font-semibold text-white">Product</h3>
          <ul className="mt-4 space-y-3">
            <li><a className="text-sm text-gray-400 hover:text-white" href="#">Courses</a></li>
            <li><a className="text-sm text-gray-400 hover:text-white" href="#">Pricing</a></li>
            <li><a className="text-sm text-gray-400 hover:text-white" href="#">Features</a></li>
          </ul>
        </div>

        <div>
          <h3 className="font-semibold text-white">Company</h3>
          <ul className="mt-4 space-y-3">
            <li><a className="text-sm text-gray-400 hover:text-white" href="#">About Us</a></li>
            <li><a className="text-sm text-gray-400 hover:text-white" href="#">Careers</a></li>
            <li><a className="text-sm text-gray-400 hover:text-white" href="#">Contact</a></li>
          </ul>
        </div>

        <div>
          <h3 className="font-semibold text-white">Legal</h3>
          <ul className="mt-4 space-y-3">
            <li><a className="text-sm text-gray-400 hover:text-white" href="#">Privacy Policy</a></li>
            <li><a className="text-sm text-gray-400 hover:text-white" href="#">Terms of Service</a></li>
          </ul>
        </div>
      </div>

      <div className="mt-12 border-t border-white/10 pt-8 text-center text-sm text-gray-500">
        <p>© 2024 AMEP. All rights reserved.</p>
      </div>
    </footer>
  );
}

export default function App() {
  return (
    <div className="bg-background-dark font-display text-white antialiased min-h-screen">
      <div className="relative w-full overflow-x-hidden">
        <div className="mx-auto flex max-w-6xl flex-col px-4 sm:px-6 lg:px-8">
          <Navbar />
          <main className="flex-grow">
            <HeroSection />
            <FeaturesSection />
            <ReviewsSection />
            <FAQSection />
          </main>
          <Footer />
        </div>
      </div>
    </div>
  );
}
