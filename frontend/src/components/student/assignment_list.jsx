import React from "react";

export default function AssignmentsPage() {
  const assignments = [
    {
      title: "Chapter 3: Kinematics Problem Set",
      course: "Advanced Mechanics",
      due: "Oct 26, 2024",
      status: "In Progress",
      difficulty: "Medium",
      color: "bg-cyan-500"
    },
    {
      title: "Lab Report: The Pendulum",
      course: "Physics 101",
      due: "Oct 22, 2024",
      status: "Submitted",
      difficulty: "Easy",
      color: "bg-green-500"
    },
    {
      title: "Final Thesis Draft",
      course: "Research Methods",
      due: "Nov 15, 2024",
      status: "Overdue",
      difficulty: "Hard",
      color: "bg-purple-600"
    },
    {
      title: "Essay: Quantum Entanglement",
      course: "Quantum Physics",
      due: "Nov 30, 2024",
      status: "Not Started",
      difficulty: "Hard",
      color: "bg-purple-600"
    },
    {
      title: "Calculus II Problem Set 5",
      course: "Mathematics II",
      due: "Nov 05, 2024",
      status: "In Progress",
      difficulty: "Easy",
      color: "bg-green-500"
    }
  ];

  const statusColor = (status) => {
    if (status === "Overdue") return "text-red-500";
    if (status === "Submitted") return "text-green-400";
    if (status === "Not Started") return "text-gray-400";
    return "text-cyan-400";
  };

  return (
    <div className="min-h-screen bg-[#0b0c10] text-white flex">
      {/* Sidebar */}
      <aside className="w-64 bg-[#0f1115] p-6 flex flex-col justify-between border-r border-gray-800">
        <div>
          <h1 className="text-xl font-bold mb-10">AMEP</h1>
          <nav className="space-y-4">
            <button className="w-full text-left text-gray-400 hover:text-white">Dashboard</button>
            <button className="w-full text-left bg-cyan-500/20 text-cyan-400 px-3 py-2 rounded-lg">Assignments</button>
            <button className="w-full text-left text-gray-400 hover:text-white">Courses</button>
            <button className="w-full text-left text-gray-400 hover:text-white">Calendar</button>
            <button className="w-full text-left text-gray-400 hover:text-white">Settings</button>
          </nav>
        </div>
        <button className="text-gray-500 hover:text-white">Logout</button>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-10">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-3xl font-semibold">Assignments</h2>
            <p className="text-gray-400 mt-1">Manage and track your AMEP coursework.</p>
          </div>

          <div className="bg-[#121318] px-4 py-2 w-80 rounded-full flex items-center">
            <span className="text-gray-400 mr-2">🔍</span>
            <input
              type="text"
              placeholder="Search assignments..."
              className="bg-transparent w-full outline-none text-sm"
            />
          </div>
        </div>

        {/* Filters */}
        <div className="flex gap-3 mb-6">
          {['All', 'In Progress', 'Submitted', 'Overdue'].map((f, i) => (
            <button
              key={i}
              className={`px-4 py-2 rounded-full text-sm ${i === 0 ? 'bg-cyan-500 text-black' : 'bg-[#121318]'}`}
            >
              {f}
            </button>
          ))}
        </div>

        {/* Table */}
        <div className="bg-[#121318] rounded-2xl p-6 shadow-lg overflow-hidden">
          <table className="w-full text-left">
            <thead>
              <tr className="text-gray-500 text-sm">
                <th className="pb-3">ASSIGNMENT TITLE</th>
                <th>COURSE</th>
                <th>DUE DATE</th>
                <th>STATUS</th>
                <th>DIFFICULTY</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800">
              {assignments.map((a, i) => (
                <tr key={i} className="py-4 h-14">
                  <td className="py-4">{a.title}</td>
                  <td>{a.course}</td>
                  <td>{a.due}</td>
                  <td className={statusColor(a.status)}>{a.status}</td>
                  <td>
                    <span className={`px-3 py-1 rounded-full text-sm ${a.color}`}>{a.difficulty}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Floating Button */}
        <button className="fixed bottom-10 right-10 bg-cyan-500 w-14 h-14 rounded-full text-black text-3xl flex items-center justify-center shadow-xl">
          +
        </button>
      </main>
    </div>
  );
}