/**
 * HTML5 & CSS3 Demo Application
 * Demonstrates modern web APIs and features
 */

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeCanvas();
    initializeAnimations();
    console.log('✅ HTML5 & CSS3 Demo initialized');
});

/**
 * Canvas API Demo - Draw animated graphics
 */
function initializeCanvas() {
    const canvas = document.getElementById('demo-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Clear canvas
    ctx.fillStyle = '#1a1a25';
    ctx.fillRect(0, 0, width, height);
    
    // Draw gradient circle
    const gradient = ctx.createRadialGradient(150, 100, 20, 150, 100, 80);
    gradient.addColorStop(0, '#7c3aed');
    gradient.addColorStop(1, '#2563eb');
    
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(150, 100, 60, 0, Math.PI * 2);
    ctx.fill();
    
    // Draw rectangle with shadow
    ctx.shadowColor = 'rgba(37, 211, 102, 0.5)';
    ctx.shadowBlur = 20;
    ctx.fillStyle = '#25D366';
    ctx.fillRect(50, 140, 80, 40);
    
    // Reset shadow
    ctx.shadowBlur = 0;
    
    // Draw text
    ctx.fillStyle = '#f0f0f5';
    ctx.font = 'bold 16px Outfit, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Canvas API Demo', 150, 30);
    
    // Animate canvas with performance optimization
    let angle = 0;
    let animationId = null;
    let isAnimating = false;
    
    function animate() {
        // Clear previous frame
        ctx.fillStyle = '#1a1a25';
        ctx.fillRect(0, 0, width, height);
        
        // Redraw static elements
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(150, 100, 60, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.shadowColor = 'rgba(37, 211, 102, 0.5)';
        ctx.shadowBlur = 20;
        ctx.fillStyle = '#25D366';
        ctx.fillRect(50, 140, 80, 40);
        ctx.shadowBlur = 0;
        
        // Draw animated line
        ctx.strokeStyle = '#f59e0b';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(width - 100, height / 2);
        ctx.lineTo(width - 100 + Math.cos(angle) * 40, height / 2 + Math.sin(angle) * 40);
        ctx.stroke();
        
        angle += 0.05;
        
        if (isAnimating) {
            animationId = requestAnimationFrame(animate);
        }
    }
    
    // Use Intersection Observer to pause animation when canvas is not visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                isAnimating = true;
                animate();
            } else {
                isAnimating = false;
                if (animationId) {
                    cancelAnimationFrame(animationId);
                }
            }
        });
    }, { threshold: 0.1 });
    
    observer.observe(canvas);
    
    // Stop animation when page is hidden (tab switching)
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            isAnimating = false;
            if (animationId) {
                cancelAnimationFrame(animationId);
            }
        } else if (canvas.getBoundingClientRect().top < window.innerHeight) {
            isAnimating = true;
            animate();
        }
    });
}

/**
 * Initialize scroll animations
 */
function initializeAnimations() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe demo cards
    document.querySelectorAll('.demo-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(card);
    });
}

// Add animation in class
const style = document.createElement('style');
style.textContent = `
    .animate-in {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
`;
document.head.appendChild(style);

/**
 * Form submission handler
 */
function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    
    console.log('Form submitted:', data);
    showNotification('✅ Form submitted successfully! Check console for data.', 'success');
    
    // Reset form after 2 seconds
    setTimeout(() => {
        event.target.reset();
        document.getElementById('range-value').textContent = '50';
    }, 2000);
}

/**
 * Local Storage Demo
 */
function saveToLocalStorage() {
    const input = document.getElementById('storage-input');
    const value = input.value.trim();
    
    if (!value) {
        showNotification('⚠️ Please enter some text first', 'warning');
        return;
    }
    
    try {
        localStorage.setItem('demo-data', value);
        localStorage.setItem('demo-timestamp', new Date().toISOString());
        showNotification('✅ Data saved to localStorage', 'success');
        updateStorageOutput();
    } catch (error) {
        showNotification('❌ Error saving to localStorage: ' + error.message, 'error');
    }
}

function loadFromLocalStorage() {
    try {
        const data = localStorage.getItem('demo-data');
        const timestamp = localStorage.getItem('demo-timestamp');
        
        if (data) {
            document.getElementById('storage-input').value = data;
            showNotification('✅ Data loaded from localStorage', 'success');
            updateStorageOutput();
        } else {
            showNotification('ℹ️ No data found in localStorage', 'info');
        }
    } catch (error) {
        showNotification('❌ Error loading from localStorage: ' + error.message, 'error');
    }
}

function clearLocalStorage() {
    try {
        localStorage.removeItem('demo-data');
        localStorage.removeItem('demo-timestamp');
        document.getElementById('storage-input').value = '';
        showNotification('✅ localStorage cleared', 'success');
        updateStorageOutput();
    } catch (error) {
        showNotification('❌ Error clearing localStorage: ' + error.message, 'error');
    }
}

function updateStorageOutput() {
    const output = document.getElementById('storage-output');
    const data = localStorage.getItem('demo-data');
    const timestamp = localStorage.getItem('demo-timestamp');
    
    if (data) {
        const date = new Date(timestamp);
        output.textContent = `Stored: "${data}" (Saved: ${date.toLocaleString()})`;
    } else {
        output.textContent = 'No data in localStorage';
    }
}

// Initialize storage output
if (document.getElementById('storage-output')) {
    updateStorageOutput();
}

/**
 * Geolocation API Demo
 */
function getLocation() {
    const output = document.getElementById('location-output');
    
    if (!navigator.geolocation) {
        output.textContent = '❌ Geolocation is not supported by your browser';
        showNotification('❌ Geolocation not supported', 'error');
        return;
    }
    
    output.textContent = '📍 Getting your location...';
    showNotification('📍 Requesting location access...', 'info');
    
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const { latitude, longitude, accuracy } = position.coords;
            output.textContent = `✅ Latitude: ${latitude.toFixed(6)}, Longitude: ${longitude.toFixed(6)}\nAccuracy: ${accuracy.toFixed(0)} meters`;
            showNotification('✅ Location retrieved successfully', 'success');
        },
        (error) => {
            let message = '';
            switch (error.code) {
                case error.PERMISSION_DENIED:
                    message = '❌ User denied the request for Geolocation';
                    break;
                case error.POSITION_UNAVAILABLE:
                    message = '❌ Location information is unavailable';
                    break;
                case error.TIMEOUT:
                    message = '❌ The request to get user location timed out';
                    break;
                default:
                    message = '❌ An unknown error occurred';
            }
            output.textContent = message;
            showNotification(message, 'error');
        },
        {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        }
    );
}

/**
 * Drag and Drop API Demo
 */
let draggedData = null;

function handleDragStart(event) {
    draggedData = event.target.textContent;
    event.dataTransfer.effectAllowed = 'move';
    event.dataTransfer.setData('text/plain', draggedData);
    event.target.style.opacity = '0.5';
}

function handleDragOver(event) {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
    event.currentTarget.classList.add('drag-over');
}

function handleDragLeave(event) {
    event.currentTarget.classList.remove('drag-over');
}

function handleDrop(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('drag-over');
    
    const data = event.dataTransfer.getData('text/plain');
    const dropZone = event.currentTarget;
    
    // Update drop zone content
    dropZone.textContent = `✅ Dropped: "${data}"`;
    dropZone.style.background = 'rgba(37, 211, 102, 0.2)';
    dropZone.style.borderColor = '#25D366';
    
    showNotification('✅ Item dropped successfully!', 'success');
    
    // Reset after 3 seconds
    setTimeout(() => {
        dropZone.textContent = 'Drop here';
        dropZone.style.background = '';
        dropZone.style.borderColor = '';
        
        // Reset dragged element
        const dragSource = document.querySelector('.drag-source');
        if (dragSource) dragSource.style.opacity = '1';
    }, 3000);
}

// Reset drag source opacity when drag ends
document.addEventListener('dragend', (event) => {
    if (event.target.classList.contains('drag-source')) {
        event.target.style.opacity = '1';
    }
});

/**
 * Show notification toast
 */
function showNotification(message, type = 'info') {
    // Remove existing notification
    const existing = document.querySelector('.notification-toast');
    if (existing) existing.remove();
    
    // Create notification
    const toast = document.createElement('div');
    toast.className = `notification-toast ${type}`;
    
    // Set background color based on type
    let bgColor = '#7c3aed'; // info
    if (type === 'success') bgColor = '#25D366';
    if (type === 'warning') bgColor = '#f59e0b';
    if (type === 'error') bgColor = '#ef4444';
    
    toast.innerHTML = `
        <span class="toast-message">${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    // Add styles
    toast.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${bgColor};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        display: flex;
        align-items: center;
        gap: 1rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease;
        font-family: 'Outfit', sans-serif;
        max-width: 400px;
    `;
    
    // Add animation keyframes if not exists
    if (!document.querySelector('#toast-styles')) {
        const style = document.createElement('style');
        style.id = 'toast-styles';
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            .toast-close {
                background: transparent;
                border: none;
                color: white;
                font-size: 1.5rem;
                cursor: pointer;
                line-height: 1;
                opacity: 0.7;
                padding: 0;
                margin: 0;
            }
            .toast-close:hover { opacity: 1; }
            .toast-message {
                flex: 1;
                line-height: 1.4;
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.style.animation = 'slideIn 0.3s ease reverse';
            setTimeout(() => toast.remove(), 300);
        }
    }, 5000);
}

/**
 * Session Storage Demo (similar to localStorage)
 */
function demonstrateSessionStorage() {
    // Session storage is cleared when the page session ends
    sessionStorage.setItem('demo-session', 'This will be cleared when tab closes');
    console.log('Session storage:', sessionStorage.getItem('demo-session'));
}

demonstrateSessionStorage();

/**
 * Console logging for debugging
 */
console.log('%c HTML5 & CSS3 Demo Features ', 'background: #7c3aed; color: white; padding: 10px; font-size: 16px; font-weight: bold;');
console.log('✓ Semantic HTML5 elements');
console.log('✓ New form input types');
console.log('✓ Canvas API for 2D graphics');
console.log('✓ SVG graphics');
console.log('✓ Web Storage (localStorage & sessionStorage)');
console.log('✓ Geolocation API');
console.log('✓ Drag and Drop API');
console.log('✓ CSS3 Grid & Flexbox layouts');
console.log('✓ CSS3 animations & transitions');
console.log('✓ CSS3 gradients, shadows, and effects');
console.log('✓ Media queries for responsive design');
