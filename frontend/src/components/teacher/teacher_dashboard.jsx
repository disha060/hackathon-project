import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { FiSearch, FiLogOut, FiSettings } from "react-icons/fi";

const lineData = [
  { name: "WK1", value: 40 },
  { name: "WK2", value: 45 },
  { name: "WK3", value: 50 },
  { name: "WK4", value: 60 },
  { name: "WK5", value: 62 },
  { name: "WK6", value: 70 },
  { name: "WK7", value: 82 },
];

export default function DashboardPage() {
  return (
    <div className="flex bg-[#07131C] text-white min-h-screen">
      {/* SIDEBAR */}
      <aside className="w-64 bg-[#0B1A24] border-r border-gray-800 p-6 space-y-6">
        <h2 className="text-xl font-bold">📘 AMEP Dashboard</h2>

        <nav className="space-y-3 text-gray-300">
          <a className="block p-2 rounded-lg bg-[#122833] text-white">Dashboard</a>
          <a className="block p-2 hover:bg-[#122833] rounded-lg">Students</a>
          <a className="block p-2 hover:bg-[#122833] rounded-lg">Classes</a>
          <a className="block p-2 hover:bg-[#122833] rounded-lg">Messaging</a>
          <a className="block p-2 hover:bg-[#122833] rounded-lg">Reports</a>
          <a className="block p-2 hover:bg-[#122833] rounded-lg">Resources</a>
        </nav>

        <div className="mt-20 space-y-4 text-gray-400">
          <button className="flex items-center gap-2 hover:text-white">
            <FiSettings /> Settings
          </button>
          <button className="flex items-center gap-2 hover:text-white">
            <FiLogOut /> Logout
          </button>
        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="flex-1 p-8">
        {/* TOP BAR */}
        <div className="flex justify-between items-center mb-10">
          <div className="relative w-1/2">
            <FiSearch className="absolute left-3 top-3 text-gray-400" />
            <input
              type="text"
              placeholder="Search students, classes..."
              className="w-full bg-[#0E1E28] rounded-lg pl-10 py-2 outline-none border border-gray-700 text-sm"
            />
          </div>

          <div className="flex items-center gap-3">
            <img
              src="https://via.placeholder.com/40"
              className="w-10 h-10 rounded-full"
              alt=""
            />
            <div>
              <p className="font-semibold">Jane Doe</p>
              <p className="text-xs text-gray-400">AMEP Teacher</p>
            </div>
          </div>
        </div>

        <h1 className="text-3xl font-bold mb-6">Welcome, Jane!</h1>

        {/* STATS CARDS */}
        <div className="grid grid-cols-3 gap-6 mb-10">
          <StatCard title="Total Students" value="124" change="+2% this month" />
          <StatCard title="Overall Attendance" value="92%" change="+1.5% from last week" />
          <StatCard title="Average Class Score" value="85%" change="-0.5% from last exam" negative />
        </div>

        {/* STUDENTS + DEADLINES SECTION */}
        <div className="grid grid-cols-2 gap-8 mb-10">
          {/* Students Needing Attention */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Students Needing Attention</h2>
            <div className="space-y-4">
              <AttentionCard
                name="David Chen"
                issue="Low Attendance"
                color="yellow"
                details="David has missed 6 of the last 10 classes. Intervention may be required."
              />
              <AttentionCard
                name="Maria Rodriguez"
                issue="Failing Grade"
                color="red"
                details="Maria’s average score has dropped to 45% and needs parent-teacher meeting."
              />
            </div>
          </div>

          {/* Upcoming Deadlines */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Upcoming Deadlines</h2>
            <div className="space-y-4">
              <DeadlineCard title="History Essay Submission" date="Tomorrow, 11:30 PM" color="blue" />
              <DeadlineCard title="Math Quiz Grading" date="Due in 2 days" color="green" />
              <DeadlineCard title="Science Lab Reports" date="Due in 5 days" color="purple" />
            </div>
          </div>
        </div>

        {/* PERFORMANCE TRENDS */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Class Performance Trends</h2>
          <div className="bg-[#091821] p-6 rounded-xl border border-gray-800">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={lineData}>
                <XAxis dataKey="name" stroke="#5A728A" />
                <YAxis stroke="#5A728A" />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#4CC9F0" strokeWidth={3} dot />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </main>
    </div>
  );
}

/* SMALL COMPONENTS -------- */

function StatCard({ title, value, change, negative }) {
  return (
    <div className="bg-[#0D2A32] p-6 rounded-xl shadow-md">
      <p className="text-gray-400 text-sm">{title}</p>
      <p className="text-3xl font-bold mt-2">{value}</p>
      <p className={`text-xs mt-1 ${negative ? "text-red-400" : "text-green-400"}`}>
        {change}
      </p>
    </div>
  );
}

function AttentionCard({ name, issue, color, details }) {
  const colorMap = {
    yellow: "bg-yellow-600",
    red: "bg-red-600",
    blue: "bg-blue-600",
  };

  return (
    <div className="p-5 bg-[#0D2A32] rounded-xl border border-gray-700">
      <div className="flex items-center gap-4">
        <div className="w-12 h-12 rounded-full bg-gray-700"></div>
        <div>
          <p className="font-semibold">{name}</p>
          <div className={`text-xs px-2 py-1 rounded ${colorMap[color]} w-fit mt-1`}>
            {issue}
          </div>
        </div>
      </div>
      <p className="text-gray-300 text-sm mt-3">{details}</p>
      <button className="mt-3 px-4 py-1 bg-cyan-600 rounded-lg text-sm hover:bg-cyan-500">
        View Profile
      </button>
    </div>
  );
}

function DeadlineCard({ title, date, color }) {
  const colorMap = {
    blue: "bg-blue-600",
    green: "bg-green-600",
    purple: "bg-purple-600",
  };

  return (
    <div className="p-4 bg-[#0D2A32] rounded-xl border border-gray-700 flex items-start gap-4">
      <div className={`w-10 h-10 rounded-full ${colorMap[color]} flex-shrink-0`}></div>
      <div>
        <p className="font-semibold">{title}</p>
        <p className="text-gray-400 text-xs">{date}</p>
      </div>
    </div>
  );
}
