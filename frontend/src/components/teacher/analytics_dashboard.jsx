import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const engagementData = [
  { day: "Mon", value: 3200 },
  { day: "Tue", value: 4500 },
  { day: "Wed", value: 3800 },
  { day: "Thu", value: 5200 },
  { day: "Fri", value: 4800 },
  { day: "Sat", value: 3000 },
  { day: "Sun", value: 4900 },
];

export default function AnalyticsDashboard() {
  return (
    <div className="min-h-screen bg-[#0B121B] text-white p-6 flex gap-6">
      {/* Sidebar */}
      <div className="w-64 bg-[#0F1724] rounded-2xl p-6 flex flex-col justify-between">
        <div>
          <h2 className="text-xl font-bold mb-6">AMEP Analytics</h2>

          <nav className="space-y-3 text-gray-300">
            {['Overview','Courses','Students','Reports'].map((item,i)=>(
              <div key={i} className={`p-3 rounded-xl cursor-pointer ${i===0? 'bg-[#1A2234] text-white':'hover:bg-[#1A2234]'}`}>{item}</div>
            ))}
          </nav>
        </div>

        <button className="bg-teal-500 hover:bg-teal-600 w-full py-3 rounded-xl font-semibold mt-6">
          Generate Report
        </button>
      </div>

      {/* Main Content */}
      <div className="flex-1 space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Analytics Dashboard</h1>
          <select className="bg-[#0F1724] px-4 py-2 rounded-xl border border-gray-700">
            <option>Last 30 Days</option>
            <option>Last 7 Days</option>
            <option>Last 90 Days</option>
          </select>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-4 gap-6">
          {[
            { label: "Total Student Enrollment", value: "12,450", trend: "+5.2%" },
            { label: "Active Users Today", value: "852", trend: "+1.5%" },
            { label: "Overall Course Completion", value: "88%", trend: "-0.5%" },
            { label: "Avg. Assessment Score", value: "92%", trend: "+2.1%" },
          ].map((card, i) => (
            <div key={i} className="bg-[#0F1724] p-5 rounded-2xl border border-[#1E2A3A]">
              <p className="text-gray-400 text-sm">{card.label}</p>
              <h2 className="text-3xl font-bold mt-2">{card.value}</h2>
              <p className={`text-sm mt-1 ${card.trend.includes('-') ? 'text-red-400' : 'text-green-400'}`}>{card.trend}</p>
            </div>
          ))}
        </div>

        {/* Graph + Top Courses */}
        <div className="grid grid-cols-3 gap-6">
          <div className="col-span-2 bg-[#0F1724] p-6 rounded-2xl border border-[#1E2A3A]">
            <h2 className="text-xl font-bold mb-1">Student Engagement Over Time</h2>
            <p className="text-gray-300 mb-4">78,923 Active Hours</p>

            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={engagementData}>
                <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
                <XAxis dataKey="day" stroke="#aaa" />
                <YAxis stroke="#aaa" />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#00E5FF" strokeWidth={3} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-[#0F1724] p-6 rounded-2xl border border-[#1E2A3A]">
            <h2 className="text-xl font-semibold mb-4">Top Performing Courses</h2>
            {[
              { name: "Advanced Concepts", val: 98 },
              { name: "Practical Applications", val: 95 },
              { name: "Intro to AMEP", val: 92 },
              { name: "Final Project", val: 87 },
            ].map((c, i) => (
              <div key={i} className="mb-4">
                <div className="flex justify-between mb-1 text-gray-300 text-sm">
                  <span>{c.name}</span>
                  <span>{c.val}%</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div className="bg-teal-400 h-2 rounded-full" style={{ width: `${c.val}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Heatmap */}
        <div className="bg-[#0F1724] p-6 rounded-2xl border border-[#1E2A3A]">
          <h2 className="text-xl font-semibold mb-4">Peak Activity Heatmap</h2>
          <div className="grid grid-cols-8 gap-4 text-sm text-gray-400">
            <div></div>
            {["Sun","Mon","Tue","Wed","Thu","Fri","Sat"].map((d,i)=>(<div key={i}>{d}</div>))}

            {[
              "8am","10am","12pm","2pm","4pm","6pm","8pm"
            ].map((t,i)=>(
              <React.Fragment key={i}>
                <div className="text-gray-400">{t}</div>
                {[...Array(7)].map((_,j)=>(
                  <div key={j} className="h-4 rounded-md bg-teal-500 opacity-40"></div>
                ))}
              </React.Fragment>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}