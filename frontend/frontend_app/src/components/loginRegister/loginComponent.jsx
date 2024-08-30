import React, { useState } from "react";
import ReactDOM from 'react-dom/client';
import login_images from '../../assets/images/login_side_images.jpeg';
import styles from '../../styles/loginRegister/registerNewUser.css';

function LogIn() {
    console.log("login");

    const [userName, setUserName] = useState('');
    const [password, setPassword] = useState('');
    const [passwordError, setPasswordError] = useState(''); // To display password validation errors

    const validatePassword = (password) => {
        const minLength = 10;
        const hasUppercase = /[A-Z]/.test(password);
        const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        const hasThreeNumbers = (password.match(/\d/g) || []).length >= 3;
        const lengthValid = password.length >= minLength;

        if (!lengthValid) {
            return "Password must be at least 10 characters long.";
        }
        if (!hasUppercase) {
            return "Password must contain at least one uppercase letter.";
        }
        if (!hasSpecialChar) {
            return "Password must contain at least one special character.";
        }
        if (!hasThreeNumbers) {
            return "Password must contain at least three numbers.";
        }
        return ""; // No errors
    };

    const handlePasswordChange = (e) => {
        const newPassword = e.target.value;
        setPassword(newPassword);
        const validationError = validatePassword(newPassword);
        setPasswordError(validationError);
    };

    const handleClick = () => {
        if (passwordError) {
            console.log("Cannot submit, password is invalid.");
        } else {
            console.log("Password is valid.");
            // Add your submission logic here
            setUserName(''); // Reset userName
            setPassword(''); // Reset password
        }
    };

    return (
        <>
            <div className="register-main-div">
                <div className="side-image-content">
                    {/* <img className="side-image" src={login_images} alt="no image to display"/> */}
                </div>

                <div className="side-login-content">
                    <div className="inner-box-of-side-login-content">
                        <div className="username-div">
                            <input
                                type="text"
                                className="username-field"
                                placeholder="Enter user email"
                                value={userName}
                                onChange={(e) => setUserName(e.target.value)}
                            />
                        </div>
                        <div className="password-div">
                            <input
                                type="password"
                                className="password-field"
                                placeholder="Enter Your Password"
                                value={password}
                                onChange={handlePasswordChange}
                            />
                            {passwordError && <p className="error-message">{passwordError}</p>}
                        </div>
                        <div>
                            <input
                                type="submit"
                                value="submit"
                                onClick={handleClick}
                            />
                            { <p> Cannot have Account ?  <a href = "" >sign-up !</a></p>}
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}

export default LogIn;
