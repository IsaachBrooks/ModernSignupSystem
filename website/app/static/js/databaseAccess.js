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

export async function getSectionsInfo(sectionList) {
    const url = `/api/getSectionsInfo/[${sectionList}]`;
    try {
        const response = await fetch(url);
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.log(error);
    }
}

export async function getSectionInfo(crn) {
    const url = `/api/getSectionInfo/${crn}`;
    try {
        const response = await fetch(url);
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.log(error);
    }
}

export async function getClassInfo(cID) {
    const url = `/api/getClassInfo/${cID}`;
    try {
        const response = await fetch(url);
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.log(error);
    }
}

export async function getClassInfoMinimal(cID) {
    const url = `/api/getClassInfoMinimal/${cID}`;
    try {
        const response = await fetch(url);
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.log(error);
    }
}

export async function enrollStudent(crn) {
    const url = '/api/enrollStudent';
    let data = {'crn': crn};
    console.log(crn)
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(data),
            cache: 'no-cache',
            credentials: 'include',
            headers: {
                "content-type": "application/json"
            }
        });
        if (response.ok) {
            console.log(crn);
        }
    } catch (error) {
        console.log(error)
    }
}

export async function getCurStudentSections() {
    const url = '/api/getCurStudentSections';
    try {
        const response = await fetch(url);
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.log(error);
    }
}