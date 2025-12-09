import React from "react";

export default function StudentProgress() {
  const mastery = [
    { label: "Reading Comprehension", value: 92 },
    { label: "Conversational English", value: 85 },
    { label: "Grammar & Vocabulary", value: 88 },
    { label: "Writing Skills", value: 45 },
  ];

  return (
    <div className="min-h-screen w-full bg-[#0b0f19] text-white p-8">
      {/* Breadcrumb */}
      <p className="text-gray-400 mb-4 text-sm">Students / Jane Doe’s Progress</p>

      {/* Header Card */}
      <div className="bg-gradient-to-r from-[#1d1f33] to-[#0f172a] p-6 rounded-2xl shadow-xl flex items-center justify-between mb-8">
        <div className="flex items-center gap-4">
          <img
            src="https://i.pravatar.cc/100"
            alt="profile"
            className="w-16 h-16 rounded-full"
          />
          <div>
            <h2 className="text-2xl font-semibold">Jane Doe</h2>
            <p className="text-gray-400 text-sm">Student ID: 4582-901B</p>
          </div>
        </div>
        <button className="px-5 py-2 bg-blue-600 rounded-xl text-white shadow-lg hover:bg-blue-700">
          Intervene
        </button>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {[ 
          { label: "Current Streak", value: "15 Days", change: "+2%", color: "text-green-400" },
          { label: "Overall Mastery", value: "82%", change: "-1%", color: "text-red-400" },
          { label: "Active Risk Alerts", value: "2", change: "+1%", color: "text-purple-400" },
          { label: "Time This Week", value: "6h 42m", change: "+15m", color: "text-green-400" },
        ].map((s, i) => (
          <div
            key={i}
            className="bg-[#111827] p-5 rounded-2xl shadow-xl border border-gray-800"
          >
            <p className="text-gray-400 text-sm">{s.label}</p>
            <h3 className="text-2xl font-bold mt-1">{s.value}</h3>
            <p className={`text-xs mt-1 ${s.color}`}>{s.change}</p>
          </div>
        ))}
      </div>

      {/* Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chart */}
        <div className="lg:col-span-2 bg-[#111827] rounded-2xl p-6 border border-gray-800 shadow-xl">
          <h3 className="text-lg font-semibold mb-4">Progress Over Time</h3>
          <div className="w-full h-[380px] bg-black/30 rounded-xl flex items-center justify-center text-gray-500">
            {/* Placeholder for graph */}
            <p>Graph Placeholder</p>
          </div>
        </div>

        {/* Subject Mastery */}
        <div className="bg-[#111827] rounded-2xl p-6 border border-gray-800 shadow-xl">
          <h3 className="text-lg font-semibold mb-4">Subject Mastery</h3>

          <div className="space-y-4">
            {mastery.map((m, i) => (
              <div key={i}>
                <div className="flex justify-between mb-1">
                  <span className="text-gray-300 text-sm">{m.label}</span>
                  <span className="text-sm font-semibold">{m.value}%</span>
                </div>
                <div className="w-full bg-gray-700/40 h-2 rounded-full">
                  <div
                    className="h-2 rounded-full bg-gradient-to-r from-blue-500 to-purple-500"
                    style={{ width: `${m.value}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}