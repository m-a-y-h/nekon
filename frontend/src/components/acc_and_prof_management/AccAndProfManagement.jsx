import React, { useState } from 'react';
import AddDishForm from './AddDishForm';
import DishManagement from './DishManagement';
import LoginForm from './LoginComponent';
import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin, FaBars,FaLanguage, FaPalette } from 'react-icons/fa'; 
import backgroundImage from '../../assets/a.jpg';
import SearchAndDiscovery from '../../components/search_and_discovery/SearchAndDiscovery';

const AccAndProfManagement = () => {
    const [showDiscover, setDiscover] = useState(false);
    const [showForm, setShowForm] = useState(false);
    const [language, setLanguage] = useState('en');
    const [theme, setTheme] = useState('red');
    const [showLogin, setShowLogin] = useState(false);
    const [menuOpen, setMenuOpen] = useState(false); 

    const toggleLanguage = () => {
        setLanguage(prev => (prev === 'en' ? 'fr' : 'en'));
        closeMenu(); // Close menu when switching language
    };

    const toggleTheme = () => {
        setTheme(prevTheme =>
            prevTheme === 'white' ? 'green' : prevTheme === 'green' ? 'black' : 'white'
        );
        closeMenu(); // Close menu when switching theme
    };

    const closeMenu = () => {
        setMenuOpen(false); // Close the menu
    };

    const toggleMenu = () => {
        setMenuOpen(!menuOpen);
    };

    const getThemeClass = () => {
        switch (theme) {
            case 'white':
                return 'bg-white-100';
            case 'green':
                return 'bg-green-100';
            case 'black':
                return 'bg-black text-white';
            default:
                return 'bg-white-100';
        }
    };

    return (
        <div className={`relative min-h-screen p-5 ${getThemeClass()}`}>
            <div className="absolute inset-0">
                <img
                    src={backgroundImage}
                    alt="Background"
                    className="w-full h-full object-cover opacity-25"
                />
            </div>
            <div className="relative z-10">
                <h1 className="text-3xl font-bold text-center mb-5">
                    {language === 'en' ? 'Account and Profile Management' : 'Gestion des comptes et des profils'}
                </h1>

                <div className="flex justify-between items-center mb-5">
                    <button className="md:hidden text-white" onClick={toggleMenu}>
                        <FaBars className="text-xl" />
                    </button>

                    {/* Mobile Menu */}
                    <div className={`flex ${menuOpen ? 'flex-col absolute w-full bg-gray-800 rounded-md p-4' : 'hidden'} md:flex`}>
                    
                        <button onClick={() => { setShowLogin(!showLogin); closeMenu(); }} className="bg-blue-500 text-white px-4 py-2 rounded mb-4 mr-4">
                            {showLogin ? (language === 'en' ? 'Close Login' : 'Fermer la connexion') : (language === 'en' ? 'Login' : 'Se connecter')}
                        </button>
                        <button onClick={() => { setShowForm(!showForm); closeMenu(); }} className="bg-blue-500 text-white px-4 py-2 rounded mb-4">
                            {showForm ? (language === 'en' ? 'Hide Form' : 'Masquer le formulaire') : (language === 'en' ? 'Add New Dish' : 'Ajouter un nouveau plat')}
                        </button>

                    </div>
                </div>
                <div className="flex justify-center">
                <button 
                    onClick={() => {
                        setDiscover(!showDiscover);
                        closeMenu(); // Assuming this is a function to close the menu
                }} 
                    className="flex items-center bg-yellow-500 text-white px-4 py-2 rounded mr-4">
                    {showDiscover ? (language === 'en' ? 'Hide' : 'Cacher') : (language === 'en' ? 'Discover' : 'Découvrir')}
                </button>
                <button onClick={toggleLanguage} className="flex items-center bg-yellow-500 text-white px-4 py-2 rounded mr-4">
                    <FaLanguage className="mr-2" /> {/* Language icon */}
                </button>
                <button onClick={toggleTheme} className="flex items-center bg-purple-500 text-white px-4 py-2 rounded">
                    <FaPalette className="mr-2" /> {/* Theme icon */}
                </button>
                </div>
                {showLogin && <LoginForm />}
                {showForm && <AddDishForm />}
                {showDiscover && <SearchAndDiscovery onClose={() => setDiscover(false)}/>}
                <DishManagement />
            </div>

            <footer className="relative z-10 bg-gray-800 text-white py-4 mt-10 text-center">
                <p>&copy; 2024 Company. {language === 'en' ? 'All rights reserved.' : 'Tous droits réservés.'}</p>
                <p>{language === 'en' ? 'Contact us at: ' : 'Contactez-nous à: '}support@example.com</p>
                <div className="flex justify-center space-x-4 mt-4">
                    <FaFacebook className="cursor-pointer" />
                    <FaTwitter className="cursor-pointer" />
                    <FaInstagram className="cursor-pointer" />
                    <FaLinkedin className="cursor-pointer" />
                </div>
            </footer>
        </div>
    );
};

export default AccAndProfManagement;
