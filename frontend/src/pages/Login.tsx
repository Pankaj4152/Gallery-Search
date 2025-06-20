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
    <div>
      <h1>Login</h1>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div>
          <label>Username</label>
          <input {...register("username", { required: true })} />
          {errors.username && <span>This field is required</span>}
        </div>
        <div>
          <label>Password</label>
          <input {...register("password", { required: true })} type="password" />
          {errors.password && <span>This field is required</span>}
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}