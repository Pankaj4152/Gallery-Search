import { useForm } from "react-hook-form";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

export function Signup() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const navigate = useNavigate();

  const onSubmit = async (data: any) => {
    try {
      await axios.post("http://localhost:8000/signup/", data);
      toast.success('Signup succesful! Please login.', {
        style: {
            background: "#022c1e",
            color: "white"
        }
      });
      navigate("/login");
    } catch (err: any) {
      toast.error("Signup failed: " + JSON.stringify(err.response?.data), {
        style: {
          background: "#450a0a",
          color: "white",
        }
      });
      alert("Signup failed: " + JSON.stringify(err.response?.data));
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-lg">
          <div className="grid grid-cols-1 md:grid-cols-1 gap-8">
            <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow">
              <div className='p-8'>
                <div className="text-center mb-8">
                  <h1 className="text-3xl font-bold text-gray-900">Create your account</h1>
                  <p className="mt-2 text-sm text-gray-600">Join now</p>
                </div>

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Username *</label>
                    <input {...register("username", { required: true })} 
                      className={`mt-1 block w-full px-3 py-2 border ${errors.username ? 'border-red-500' : 'border-gray-300'} rounded-md shadow-sm focus:outline-none    focus:ring-indigo-500 focus:border-cyan-700`}
                      aria-invalid={errors.username ? "true" : "false"}/>
                      {errors.username && (
                        <p className="mt-2 text-sm text-red-600" role="alert">
                          <span>Username must be at least 3 characterts</span>
                        </p>
                      )}
                  </div>

                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email (optional)</label>
                    <input
                      id="email"
                      {...register("email", {
                        pattern: {
                          value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                          message: "This doesnt even works"
                        }
                      })}
                      type="email"
                      className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-cyan-700"
                    />
                    {errors.email && (
                      <p className="mt-2 text-sm text-red-600" role="alert">
                        <span>Invalid email address</span>
                      </p>
                    )}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Password *</label>
                    <input {...register("password", { required: true })} type="password" 
                    className={`mt-1 block w-full px-3 py-2 border ${errors.password ? 'border-red-500' : 'border-gray-300'} rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-cyan-700`}
                    aria-invalid={errors.password ? "true" : "false"}/>
                      {errors.password && (
                        <p className="mt-2 text-sm text-red-600" role="alert">
                          <span>8 Characters minimum</span>
                        </p>
                      )}
                  </div>
                  <button type="submit"
                    className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-cyan-700 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors">
                      Sign Up
                  </button>
                </form>

                <div className="mt-6 text-center">
                  <p className="text-sm text-gray-600">
                    Already have an account?{' '}
                    <a href="/login" className="font-medium text-cyan-700 hover:text-indigo-500">
                      Login
                    </a>
                  </p>
                </div> 
              </div>
            </div>
        </div>  
      </div>
    </div>
  );
}