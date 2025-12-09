import React from "react";

export default function ProjectDetailPage() {
  return (
    <div className="min-h-screen bg-[#021617] text-white p-6 space-y-10">
      {/* Header */}
      <header className="flex justify-between items-center py-4 px-4">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-cyan-400 rounded"></div>
          <h1 className="text-xl font-semibold">AMEP</h1>
        </div>
        <nav className="hidden md:flex space-x-8 text-gray-300 font-medium">
          <a href="#" className="hover:text-white">Dashboard</a>
          <a href="#" className="hover:text-white text-cyan-400">Projects</a>
          <a href="#" className="hover:text-white">Community</a>
          <a href="#" className="hover:text-white">Resources</a>
        </nav>
        <div className="flex items-center space-x-4">
          <button className="bg-cyan-400 text-black px-4 py-2 rounded-lg font-semibold hover:bg-cyan-300 transition">Contribute</button>
          <div className="w-9 h-9 rounded-full bg-gray-600"></div>
        </div>
      </header>

      {/* Title */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold text-cyan-300 drop-shadow-lg">AMEP Project: Futura</h1>
        <p className="text-gray-300 max-w-2xl mx-auto">
          A modern, futuristic, and highly readable interface design for the next
          generation of educational tools.
        </p>

        <div className="flex justify-center space-x-4 mt-4">
          {['In Progress', 'UI/UX', 'Web App'].map((tag) => (
            <span
              key={tag}
              className="px-4 py-1 bg-[#072629] border border-cyan-400/40 rounded-full text-cyan-300 text-sm"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Description */}
        <div className="lg:col-span-2 space-y-8">
          <section className="bg-[#072629] p-6 rounded-xl border border-gray-700/40">
            <h2 className="text-xl font-semibold mb-3">Project Description</h2>
            <p className="text-gray-300 leading-relaxed">
              Project Futura aims to redefine the user experience for our
              educational platform. By integrating cutting-edge design
              principles, we are creating an interface that is visually stunning,
              intuitive, and accessible. This project involves a complete
              overhaul focusing on streamlined navigation, enhanced readability,
              and interactive components.
            </p>
          </section>

          {/* Milestones */}
          <section className="bg-[#072629] p-6 rounded-xl border border-gray-700/40">
            <h2 className="text-xl font-semibold mb-4">Milestones</h2>
            <div className="space-y-4">
              {[
                { step: 'Phase 1: Research & Discovery', status: 'Completed' },
                { step: 'Phase 2: Wireframing & Prototyping', status: 'Completed' },
                { step: 'Phase 3: UI Design & System Build', status: 'In Progress' },
                { step: 'Phase 4: Development & Integration', status: 'Upcoming' },
                { step: 'Phase 5: Testing & Deployment', status: 'Upcoming' }
              ].map(({ step, status }) => (
                <div key={step} className="flex justify-between items-center">
                  <span className="flex items-center space-x-3">
                    <div
                      className={`w-5 h-5 rounded border flex items-center justify-center ${
                        status === 'Completed'
                          ? 'bg-cyan-400 border-cyan-400'
                          : status === 'In Progress'
                          ? 'border-cyan-300'
                          : 'border-gray-500'
                      }`}
                    >
                      {status === 'Completed' && (
                        <div className="w-3 h-3 bg-[#021617] rounded-sm"></div>
                      )}
                    </div>
                    <span className="text-gray-200">{step}</span>
                  </span>
                  <span className="text-sm text-gray-400">{status}</span>
                </div>
              ))}
            </div>
          </section>
        </div>

        {/* Right Sidebar */}
        <div className="space-y-8">
          {/* Progress */}
          <section className="bg-[#072629] p-6 rounded-xl border border-gray-700/40">
            <h2 className="text-lg font-semibold mb-4">Project Progress</h2>
            <p className="text-gray-300 text-sm mb-2">Overall Completion</p>
            <div className="w-full bg-gray-800 h-3 rounded-full overflow-hidden">
              <div className="h-full bg-cyan-400" style={{ width: '65%' }}></div>
            </div>
            <p className="text-cyan-300 mt-2 font-medium">65%</p>
          </section>

          {/* Team */}
          <section className="bg-[#072629] p-6 rounded-xl border border-gray-700/40">
            <h2 className="text-lg font-semibold mb-4">Team Members</h2>
            <div className="flex -space-x-3">
              {[1, 2, 3, 4].map((i) => (
                <div
                  key={i}
                  className="w-10 h-10 rounded-full bg-gray-500 border-2 border-[#021617]"
                ></div>
              ))}
            </div>
            <p className="text-gray-300 text-sm mt-2">+ 2 more</p>
          </section>

          {/* Actions */}
          <section className="bg-[#072629] p-6 rounded-xl border border-gray-700/40 space-y-4">
            <h2 className="text-lg font-semibold">Actions</h2>
            <button className="w-full py-2 rounded-lg bg-cyan-400 text-black font-semibold hover:bg-cyan-300 transition">
              Contribute
            </button>
            <button className="w-full py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-600 hover:bg-gray-700 transition">
              Upload Files
            </button>
            <button className="w-full py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-600 hover:bg-gray-700 transition">
              Project Chat
            </button>
          </section>
        </div>
      </div>

      {/* Footer */}
      <footer className="text-center text-gray-500 text-sm py-10">
        © 2024 AMEP. All Rights Reserved.
      </footer>
    </div>
  );
}