export function renderRowStatus(status){
    const colorStatus = {
        'PENDIENTE': 'bg-gray-300',
        'ACEPTADO': 'bg-gradient-to-r from-teal-300 to-teal-400',
        'RECHAZADO': 'bg-red-400',
        'EXTENDIDO': 'bg-gradient-to-r from-yellow-300 to-orange-300',
        'FINALIZADO': 'bg-gradient-to-r from-cyan-300 to-blue-300',
    }
    return `<span class='text-xs px-2 py-1 text-white rounded ${colorStatus[status]}'>${status}</span>`
}