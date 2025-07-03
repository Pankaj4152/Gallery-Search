import { useForm } from "react-hook-form";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

export function Login() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const navigate = useNavigate();

  const onSubmit = async (data: any) => {
    try {
      const res = await axios.post("http://localhost:8000/api/token/", data);
      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);
      toast.success('Login was succesfull. Welcome to your gallery!', {
                style: {
                    background: "#022c1e",
                    color: "white"
                }
            });
      navigate("/gallery");
    } catch (err: any) {
      toast.error("Login failed: " + JSON.stringify(err.response?.data), {
        style: {
          background: "#450a0a",
          color: "white",
        }
      });
    }
  };

  return (
    <div className="min-h-screen py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md mx-auto rounded-xl shadow-md overflow-hidden md:max-w-lg">
          <div className="grid grid-cols-1 md:grid-cols-1 gap-8">
            <div className="bg-gray-800 p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow">
              <div className='p-8'>
                <div className="text-center mb-8">
                  <h1 className="text-white text-3xl font-bold text-gray-900">Nice to see you again!</h1>
                  <p className="mt-2 text-sm text-gray-600">Sign in to your gallery</p>
                </div>

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-400">Username</label>
                    <input {...register("username", { required: true })}
                      className={`text-white mt-1 block w-full px-3 py-2 border ${errors.username ? 'border-red-500' : 'border-gray-300'} rounded-md shadow-sm focus:outline-none    focus:ring-indigo-500 focus:border-cyan-700`}
                        aria-invalid={errors.username ? "true" : "false"}/>
                        {errors.username && (
                          <p className="mt-2 text-sm text-red-600" role="alert">
                            <span>Username must be at least 3 characterts</span>
                          </p>
                      )}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-400">Password</label>
                    <input {...register("password", { required: true })} type="password" 
                      className={`text-white mt-1 block w-full px-3 py-2 border ${errors.password ? 'border-red-500' : 'border-gray-300'} rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-cyan-700`}
                      aria-invalid={errors.password ? "true" : "false"}/>
                        {errors.password && (
                          <p className="mt-2 text-sm text-red-600" role="alert">
                            <span>8 Characters minimum</span>
                          </p>
                      )}
                  </div>
                  <button type="submit" 
                    className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-cyan-700 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors">
                      Login
                  </button>
                </form>

                <div className="mt-6 text-center">
                  <p className="text-sm text-gray-600">
                    No account?{' '}
                    <a href="/signup" className="font-medium text-cyan-700 hover:text-indigo-500">
                      Sign up
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