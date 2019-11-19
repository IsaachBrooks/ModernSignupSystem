import { noOverlaps, showCanTake } from './options.js'

export default getSectionTimesDaysFull;

async function baseGetRequest(url) {
    try {
        const response = await fetch(url);
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.log(error)
    }
}

export async function getSectionTimesDaysFull() {
    const url = '/api/getSectionTimesDaysFull';
    return baseGetRequest(url);
}

export async function getStudentSectionListFull() {
    const url = '/api/getStudentSectionListFull';
    return baseGetRequest(url);
}

export async function getStudentSectionsDraw() {
    const url = '/api/getStudentSectionsDraw';
    return baseGetRequest(url);
}

export async function getSectionTimesDay() {
    const url = '/api/getSectionTimesDays';
    return baseGetRequest(url);
}

export async function getSectionsInfo(sectionList) {
    const url = `/api/getSectionsInfo/[${sectionList}]`;
    return baseGetRequest(url);
}

export async function getSectionInfo(crn) {
    const url = `/api/getSectionInfo/${crn}`;
    return baseGetRequest(url);
}

export async function getClassInfo(cID) {
    const url = `/api/getClassInfo/${cID}`;
    return baseGetRequest(url);
}

export async function getClassInfoMinimal(cID) {
    const url = `/api/getClassInfoMinimal/${cID}`;
    return baseGetRequest(url);
}

export async function enrollStudent(crn) {
    const url = '/api/enrollStudent';
    let data = {'crn': crn};
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
            return response.json();
        }
    } catch (error) {
        console.log(error)
    }
}

export async function removeEnrolledClass(crn) {
    const url = '/api/removeEnrolledClass';
    let data = {'crn': crn};
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
            return response.json();
        }
    } catch (error) {
        console.log(error)
    }
}

export async function getCurStudentSections() {
    const url = '/api/getCurStudentSections';
    return baseGetRequest(url);
}

export async function isCurStudentRegisteredFor(crn) {
    const url = `/api/isCurStudentRegisteredFor/${crn}`
    return baseGetRequest(url);
}

export async function getDepartmentNamesIDs() {
    const url = '/api/getDepartmentNamesIDs';
    return baseGetRequest(url);
}

export function getSectionsByDepartment(dpID) {
    const url = `/api/getSectionsByDepartment/dpID=${dpID}&noOverlaps=${noOverlaps}&showCanTake=${showCanTake}`;
    console.log(url);
    return baseGetRequest(url);
}

export async function searchForSections(query) {
    const url = '/api/searchForSections';
    let data = {'query': query};
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
            return response.json();
        }
    } catch (error) {
        console.log(error)
    }
}

export async function completeCurSections() {
    const url = '/api/completeCurSections';
    let data = {};
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
            return response.json();
        }
    } catch (error) {
        console.log(error);
    }
}

export async function getStudentCompleted() {
    const url = 'api/getStudentCompleted';
    return baseGetRequest(url);
}

export function showLoading() {
    let loader = $('#loading-indicator');
    loader.css('visibility', 'visible');
}

export function hideLoading() {
    let loader = $('#loading-indicator');
    loader.css('visibility', 'hidden');
}

export function getCurStudentSectionsMinimal() {
    let url = '/api/getCurStudentSectionsMinimal'
    return baseGetRequest(url);
}