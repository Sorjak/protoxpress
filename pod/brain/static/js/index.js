const action_url = '/api/actions'
async function setAction(action) {
    console.log(`Setting action ${action}`);

    const response = await fetch(action_url, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({'action': action.toLowerCase()})
    });

    if (!response.ok) { 
        console.error(response.json()); return; 
    }

    console.log(await response.json());
    return;
}

async function goToPage(page_name) {
    page_action_map = new Map([
        ['integrate', 'init'],
        ['photo-mode','photo'],
        ['party-mode','test'],
        ['danger-mode','emergency'],
        ['happy-mode','happy'],
        ['sad-mode','sad'],
        ['main-menu', 'abort']
    ]);

    if (page_action_map.has(page_name)) {
        action = page_action_map.get(page_name);
        await setAction(action);
    }

    window.location.href = `${page_name}.html`;
}