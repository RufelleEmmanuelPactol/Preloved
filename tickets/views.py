from django.shortcuts import render
from django.views import View
from datetime import datetime

from preloved_auth.models import ShopUser
from .models import Ticket, Status
from django.http import JsonResponse
from store.models import *



def return_not_post():
    return JsonResponse({'error': 'not a post-type request'}, status=400)


def thumbnailify(id):
    set = Slug.objects.filter(itemID=id, isThumbnail=1)
    if set is None:
        return 1
    return 0


# Create your views here.

def return_id_not_found():
    return JsonResponse({'error': 'Specified id not found.'}, status=400)


def return_not_auth():
    # raise Exception("User not authenticated")
    return JsonResponse({'error': 'user not authenticated'}, status=400)

# Create your views here.




class PurchaseController:

    @staticmethod
    def purchase_item(request):
        try:
            if request.method != 'POST':
                return return_not_post()
            if not request.user.is_authenticated:
                return return_not_auth()
            id = request.user.id
            shopUser = ShopUser.objects.filter(id=id).first()
            if shopUser is None:
                return JsonResponse({'error': 'user is not a shop user'}, status=400)
            itemID = int(request.POST.get('itemID'))
            storeID = int(request.POST.get('storeID'))
            storeID = Store.objects.filter(storeID=storeID).first()
            if storeID is None:
                return return_id_not_found()
            item = Item.objects.filter(itemID=itemID).first()
            if item is None:
                return_id_not_found()
            t = Ticket(itemID=item, status=Status.objects.filter(statusID=1).first(), storeID=storeID, userID =shopUser)
            item.isTaken = 1
            t.save()
            item.save()
            return JsonResponse({'response' : 'OK!', 'ticketID' : t.ticketID})
        except Exception as e:
            raise e
            return JsonResponse({'error': str(e)}, status=400)






class TicketController(View):

    def post(self, request):
        userID = request.POST.get('userID')
        itemID = request.POST.get('itemID')
        Ticket.objects.create(userID=userID, itemID=itemID, status=1)
        return JsonResponse({'status': 'OK!'})


    def get(self, request):
        ticket = {}
        ticketID = request.GET.get('ticketID', 0)
        userID = request.GET.get('userID', 0)
        if ticketID != 0:
            ticket_obj = Ticket.objects.filter(ticketID=ticketID).first()
            ticket['ticketID'] = ticket_obj.ticketID
            ticket['userID'] = ticket_obj.userID
            ticket['storeID'] = ticket_obj.storeID
            ticket['itemID'] = ticket_obj.itemID
            stat = ticket_obj.status
            status_obj = Status.objects.filter(statusID=stat).first()
            if status_obj:
                ticket['status'] = status_obj.status_name
                ticket['statusINT'] = stat
            else:
                ticket['status'] = "Status not found"
                ticket['statusINT'] = stat
            return JsonResponse(ticket)
        if userID is not None:
            tickets = Ticket.objects.filter(userID=userID)
            ticket_list = []

            for ticket_obj in tickets:
                ticket_data = {
                    'ticketID': ticket_obj.ticketID,
                    'userID': ticket_obj.userID,
                    'storeID': ticket_obj.storeID,
                    'itemID': ticket_obj.itemID,
                    'status': Status.objects.filter(statusID=ticket_obj.status).first().status_name
                }
                ticket_list.append(ticket_data)

            return JsonResponse({'tickets': ticket_list})
        else:
            return JsonResponse({'error': 'Invalid parameters'})
