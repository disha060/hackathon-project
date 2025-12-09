import React from "react";

export default function ClassManagement() {
  const students = [
    { name: "Elanor Vance", id: "ID-84231", attendance: "98%", progress: 95, status: "Active" },
    { name: "Marcus Thorne", id: "ID-73902", attendance: "93%", progress: 88, status: "Active" },
    { name: "Aria Petrova", id: "ID-91234", attendance: "85%", progress: 78, status: "Needs Attention" },
    { name: "Liam Chen", id: "ID-69042", attendance: "100%", progress: 99, status: "Active" },
    { name: "Seraphina Cruz", id: "ID-87263", attendance: "75%", progress: 66, status: "Needs Attention" },
    { name: "Celeste Dubois", id: "ID-15875", attendance: "60%", progress: 50, status: "Withdrawn" },
  ];

  const statusColors = {
    Active: "bg-green-600/20 text-green-400",
    "Needs Attention": "bg-yellow-600/20 text-yellow-400",
    Withdrawn: "bg-red-600/20 text-red-400",
  };

  return (
    <div className="min-h-screen w-full bg-[#0b0f19] text-white p-8">
      {/* Top Bar */}
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-semibold">Class Management</h1>
        <button className="px-4 py-2 bg-blue-600 rounded-xl hover:bg-blue-700">
          Add Student
        </button>
      </div>

      <p className="text-gray-400 mb-6">AMEP English Level 3 · EL3-A</p>

      {/* Filters */}
      <div className="flex gap-3 mb-6">
        <button className="px-4 py-2 bg-[#1f2937] border border-gray-700 rounded-lg text-sm">
          All Students
        </button>
        <button className="px-4 py-2 bg-[#1f2937] border border-gray-700 rounded-lg text-sm">
          Active
        </button>
        <button className="px-4 py-2 bg-[#1f2937] border border-gray-700 rounded-lg text-sm">
          Withdrawn
        </button>
      </div>

      {/* Table */}
      <div className="bg-[#111827] p-6 rounded-2xl shadow-xl overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="text-gray-400 text-sm border-b border-gray-700">
              <th className="py-3 text-left">Student Name</th>
              <th className="py-3 text-left">ID</th>
              <th className="py-3 text-left">Attendance</th>
              <th className="py-3 text-left">Progress</th>
              <th className="py-3 text-left">Status</th>
              <th className="py-3 text-left">Actions</th>
            </tr>
          </thead>

          <tbody>
            {students.map((s, i) => (
              <tr key={i} className="border-b border-gray-800 hover:bg-[#1a2332]">
                <td className="py-4">{s.name}</td>
                <td>{s.id}</td>
                <td>{s.attendance}</td>
                <td>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div
                      className="h-2 bg-blue-500 rounded-full"
                      style={{ width: `${s.progress}%` }}
                    ></div>
                  </div>
                </td>
                <td>
                  <span
                    className={`px-3 py-1 rounded-full text-sm ${statusColors[s.status]}`}
                  >
                    {s.status}
                  </span>
                </td>
                <td>
                  <button className="text-blue-400 hover:underline text-sm">
                    View Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="flex justify-center mt-6 gap-3 text-gray-300">
        {[1, 2, 3, "…", 10].map((p, i) => (
          <button
            key={i}
            className={`px-3 py-1 rounded-full ${p === 1 ? "bg-blue-600" : "bg-[#1f2937]"}`}
          >
            {p}
          </button>
        ))}
      </div>
    </div>
  );
}