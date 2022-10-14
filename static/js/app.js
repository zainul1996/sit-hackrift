(function () {
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/sw.js')
                .then(function (registration) {
                    console.log('Service Worker Registered');
                    return registration;
                })
                .catch(function (err) {
                    console.error('Unable to register service worker.', err);
                });
            navigator.serviceWorker.ready.then(function (registration) {
                console.log('Service Worker Ready');
                console.log('Service Worker Ready');
            });
        });
    }
})();


let deferredPrompt;
// const btnAdd = document.querySelector('#btnAdd');

// window.addEventListener('beforeinstallprompt', (e) => {
//     console.log('beforeinstallprompt event fired');
//     e.preventDefault();
//     deferredPrompt = e;
//     btnAdd.style.visibility = 'visible';
// });

// btnAdd.addEventListener('click', (e) => {
//     btnAdd.style.visibility = 'hidden';
//     deferredPrompt.prompt();
//     deferredPrompt.userChoice
//         .then((choiceResult) => {
//             if (choiceResult.outcome === 'accepted') {
//                 console.log('User accepted the A2HS prompt');
//             } else {
//                 console.log('User dismissed the A2HS prompt');
//             }
//             deferredPrompt = null;
//         });
// });

window.addEventListener('appinstalled', (evt) => {
    app.logEvent('app', 'installed');
});

var applicant = {
    "age": 18,
    "gender": "M",
    "MMR": "1500"
}

var application = {
    "id": 14,
    "startAge": 18,
    "endAge": 25,
    "activity": "badminton",
    "gender": ["M", "F", "O"],
    "locations": ["ss", "ps", "there"],
    "startDate": "14-10-2022",
    "endDate": "15-10-2022",
    "startDuration": 7,
    "endDuration": 9,
    "user": "hehe",
    "MMR": 1554,
    "age": 18,
    "gender": "M",
    "match": "pending",
    "rejected": [20],
    "attendance": 1
}

const btn = document.querySelector('#btn');

btn.addEventListener('click', (e) => {
    console.log("hello");
    fetch('/test', {
        headers: {
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(application)
    })
        .then((response) => response.json())
        .then((data) => console.log(data));
});