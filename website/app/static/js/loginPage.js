$(
    document.getElementById('username').onchange = () => {
        console.log(this.value);
        if (this.value === '') {
            document.getElementById('password').value = '';
        }
    }
);
