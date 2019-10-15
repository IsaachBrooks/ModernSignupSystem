

const getSectionTimesDaysFull = async () => {
    const url = '/api/getSectionTimesDaysFull';
    try {
        const response = await fetch(url);
        if (response.ok) {
            const ret = await response.json();
            return ret;
        }
    } catch (error) {
        console.log(error);
    }
}


const STDs = getSectionTimesDaysFull();

document.write(STDs.value)
