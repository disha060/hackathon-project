import React from "react";

export default function MasteryTracker() {
  const skills = [
    { title: "Advanced Grammar", percent: 95, level: "High Proficiency", color: "bg-cyan-400" },
    { title: "Fluid Dynamics Basics", percent: 65, level: "Medium Proficiency", color: "bg-blue-400" },
    { title: "Chemical Bonding", percent: 30, level: "Low Proficiency", color: "bg-purple-500" },
    { title: "Literary Analysis", percent: 88, level: "High Proficiency", color: "bg-cyan-400" },
    { title: "Quantum Mechanics", percent: 42, level: "Low Proficiency", color: "bg-purple-500" }
  ];

  return (
    <div className="min-h-screen bg-[#0b0c10] text-white p-10 font-sans">
      <header className="flex justify-between items-center mb-10">
        <h1 className="text-xl font-bold">AMEP</h1>
        <div className="w-10 h-10 bg-gray-700 rounded-full"></div>
      </header>

      <h2 className="text-3xl font-semibold mb-6">Mastery Tracker</h2>

      <div className="grid grid-cols-2 gap-6 mb-8">
        <div className="bg-[#121318] p-6 rounded-2xl shadow-xl">
          <p className="text-sm text-gray-400">Overall Mastery</p>
          <p className="text-4xl font-bold">72%</p>
        </div>
        <div className="bg-[#121318] p-6 rounded-2xl shadow-xl">
          <p className="text-sm text-gray-400">Skills Mastered</p>
          <p className="text-4xl font-bold">18/25</p>
        </div>
      </div>

      <div className="flex gap-4 mb-6">
        <button className="bg-[#121318] px-4 py-2 rounded-xl text-sm">Sort by: Mastery ▾</button>
        <button className="bg-[#121318] px-4 py-2 rounded-xl text-sm">Filter by: Topic ▾</button>
      </div>

      <div className="space-y-6">
        {skills.map((s, i) => (
          <div key={i} className="bg-[#121318] p-6 rounded-2xl shadow-xl">
            <div className="flex justify-between mb-2">
              <p className="font-medium text-lg">{s.title}</p>
              <p>{s.percent}%</p>
            </div>

            <div className="w-full h-3 bg-gray-700 rounded-full overflow-hidden mb-1">
              <div
                className={`${s.color} h-full`}
                style={{ width: `${s.percent}%` }}
              ></div>
            </div>

            <p className="text-sm text-gray-300">{s.level}</p>
          </div>
        ))}
      </div>

      <div className="mt-10 flex justify-end">
        <button className="flex items-center gap-2 bg-teal-500 text-black px-6 py-3 rounded-full font-semibold shadow-lg">
          <span>Practice Weak Areas</span>
        </button>
      </div>
    </div>
  );
}
