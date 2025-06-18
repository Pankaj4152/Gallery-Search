import { useForm } from "react-hook-form";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export function Signup() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const navigate = useNavigate();

  const onSubmit = async (data: any) => {
    try {
      await axios.post("http://localhost:8000/signup/", data);
      alert("Signup successful! Please log in.");
      navigate("/login");
    } catch (err: any) {
      alert("Signup failed: " + JSON.stringify(err.response?.data));
    }
  };

  return (
    <div>
      <h1>Sign Up</h1>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div>
          <label>Username</label>
          <input {...register("username", { required: true })} />
          {errors.username && <span>This field is required</span>}
        </div>
        <div>
          <label>Email (optional)</label>
          <input {...register("email")} type="email" />
        </div>
        <div>
          <label>Password</label>
          <input {...register("password", { required: true })} type="password" />
          {errors.password && <span>This field is required</span>}
        </div>
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}