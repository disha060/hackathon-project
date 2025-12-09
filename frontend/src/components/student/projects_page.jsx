import React from "react";

export default function ProjectsPage() {
  const projects = [
    {
      title: "Quantum Computing Simulator",
      desc: "Developing a scalable simulator for quantum algorithms to accelerate research and development in the quantum space.",
      status: "In Progress",
      statusColor: "bg-blue-500",
      barColor: "bg-cyan-400",
      dateLabel: "Deadline",
      date: "24 Dec 2024",
      team: [1, 2, 3]
    },
    {
      title: "AI Ethics Framework",
      desc: "A comprehensive framework for ensuring ethical considerations in AI development and deployment across all AMEP projects.",
      status: "Completed",
      statusColor: "bg-green-500",
      barColor: "bg-cyan-400",
      dateLabel: "Finished",
      date: "01 Mar 2024",
      team: [2, 4, 5]
    },
    {
      title: "Project Nebula",
      desc: "Next-generation data platform for real-time analytics and interstellar data visualization. Currently paused pending resource allocation.",
      status: "On Hold",
      statusColor: "bg-yellow-500",
      barColor: "bg-yellow-400",
      dateLabel: "Next Review",
      date: "TBD",
      team: [3, 4, 6]
    }
  ];

  return (
    <div className="min-h-screen bg-[#071013] text-white p-10 font-sans">
      {/* Navbar */}
      <header className="flex justify-between items-center mb-12">
        <div className="text-lg font-bold">AMEP</div>
        <nav className="flex items-center gap-8 text-gray-300">
          <button className="hover:text-white">Dashboard</button>
          <button className="hover:text-white font-semibold text-white">Projects</button>
          <button className="hover:text-white">Teams</button>
          <div className="w-10 h-10 rounded-full bg-yellow-500"></div>
        </nav>
      </header>

      {/* Page Title */}
      <h1 className="text-4xl font-semibold mb-2">AMEP Projects</h1>
      <p className="text-gray-400 mb-8">12 Active Projects</p>

      {/* Filters */}
      <div className="flex gap-4 mb-10">
        {[
          { label: "All" },
          { label: "In Progress" },
          { label: "Completed" },
          { label: "Team Alpha" }
        ].map((item, i) => (
          <button
            key={i}
            className={`px-4 py-2 rounded-full text-sm bg-[#0D1A1F] border border-gray-700 hover:border-cyan-400 hover:text-cyan-400 ${
              i === 0 ? "bg-cyan-500 text-black border-none" : ""
            }`}
          >
            {item.label} ▾
          </button>
        ))}

        <button className="ml-auto bg-cyan-500 text-black px-5 py-2 rounded-full font-semibold shadow-lg">
          + New Project
        </button>
      </div>

      {/* Project Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {projects.map((p, i) => (
          <div
            key={i}
            className="bg-[#0D1A1F] p-6 rounded-2xl border border-gray-800 shadow-xl hover:shadow-cyan-500/20 transition"
          >
            <h2 className="text-xl font-semibold mb-2">{p.title}</h2>

            {/* Status */}
            <span className={`px-3 py-1 rounded-full text-sm ${p.statusColor}`}>{p.status}</span>

            <p className="text-gray-400 text-sm mt-3 mb-4 leading-relaxed">{p.desc}</p>

            <div className="w-full h-2 bg-gray-700 rounded-full mb-4">
              <div className={`h-full rounded-full ${p.barColor}`} style={{ width: "70%" }}></div>
            </div>

            <p className="text-gray-400 text-xs">
              <span className="text-gray-500">{p.dateLabel}: </span>
              {p.date}
            </p>

            {/* Team Avatars */}
            <div className="flex mt-4">
              {p.team.map((t, id) => (
                <div
                  key={id}
                  className="w-8 h-8 rounded-full bg-gray-500 border-2 border-[#0D1A1F] -ml-2 first:ml-0"
                ></div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <footer className="mt-20 text-gray-600 text-sm flex justify-center gap-10 opacity-70">
        <button>About Us</button>
        <button>Contact</button>
        <button>Privacy Policy</button>
        <button>Terms of Service</button>
      </footer>

      <p className="text-center text-gray-600 text-xs mt-6">© 2024 AMEP. All Rights Reserved.</p>
    </div>
  );
}