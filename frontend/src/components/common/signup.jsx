import React from 'react';

const SignUpPage = () => {
  return (
    <div className="min-h-screen bg-[#eef6fb] relative overflow-hidden font-sans">
      {/* Background Decorative Blobs */}
      <div className="absolute top-[20%] left-[-5%] w-96 h-96 bg-blue-100 rounded-full blur-3xl opacity-60"></div>
      <div className="absolute bottom-[-10%] right-[-5%] w-[30rem] h-[30rem] bg-indigo-100 rounded-full blur-3xl opacity-60"></div>

      {/* Header / Navbar */}
      <header className="relative z-10 flex justify-between items-center px-8 py-6">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-slate-800 rounded-sm transform rotate-12"></div>
          <span className="font-bold text-slate-800 tracking-tight">AMEP</span>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-sm text-slate-500">Already have an account?</span>
          <button className="px-5 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors">
            Log In
          </button>
        </div>
      </header>

      {/* Main Form Container */}
      <main className="relative z-10 flex flex-col items-center justify-center pt-10 pb-20">
        <div className="w-full max-w-lg bg-white rounded-[2.5rem] shadow-xl shadow-blue-100/50 p-10 md:p-12">
          <div className="text-center mb-10">
            <h1 className="text-3xl font-bold text-slate-800 mb-2">Get Started with AMEP</h1>
            <p className="text-slate-500">Create your account to continue</p>
          </div>

          <form className="space-y-6">
            {/* Full Name */}
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Full Name</label>
              <input 
                type="text" 
                placeholder="Enter your full name" 
                className="w-full px-5 py-3 rounded-xl border border-slate-200 bg-slate-50/50 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
              />
            </div>

            {/* Email Address */}
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Email Address</label>
              <input 
                type="email" 
                placeholder="Enter your email address" 
                className="w-full px-5 py-3 rounded-xl border border-slate-200 bg-slate-50/50 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Password</label>
              <input 
                type="password" 
                placeholder="Enter your password" 
                className="w-full px-5 py-3 rounded-xl border border-slate-200 bg-slate-50/50 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
              />
            </div>

            {/* Role Select */}
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">I am a...</label>
              <div className="relative">
                <select className="w-full px-5 py-3 rounded-xl border border-slate-200 bg-slate-50/50 text-slate-700 appearance-none focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all">
                  <option>Student</option>
                  <option>Teacher</option>
                  <option>Administrator</option>
                </select>
                <div className="absolute inset-y-0 right-4 flex items-center pointer-events-none text-slate-400">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <button className="w-full py-4 bg-blue-600 text-white font-bold rounded-xl shadow-lg shadow-blue-200 hover:bg-blue-700 hover:shadow-blue-300 transition-all active:scale-[0.98]">
              Create Account
            </button>

            {/* Terms */}
            <p className="text-center text-xs text-slate-400 mt-4 leading-relaxed">
              By continuing, you agree to our <a href="#" className="text-blue-600 hover:underline">Terms of Service</a>
            </p>
          </form>
        </div>
      </main>
    </div>
  );
};

export default SignUpPage;