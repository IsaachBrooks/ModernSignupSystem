export default getSectionTimesDaysFull;

export async function getSectionTimesDaysFull() {
    const url = '/api/getSectionTimesDaysFull';
    try {
        const response = await fetch(url);
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.log(error);
    }
}

export async function getSectionTimesDay() {
    const url = '/api/getSectionTimesDays';
    try {
        const response = await fetch(url);
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.log(error);
    }
}