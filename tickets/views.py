from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
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
            tix = Ticket.objects.filter(userID_id=request.user.id, itemID=item)
            for ticket in tix:
                if ticket.status.level <= 2:
                    return JsonResponse({"error": "Cannot add item to card. Pending ticket already exists."},
                                        status=400)

            t = Ticket(itemID=item, status=Status.objects.filter(statusID=1).first(), storeID=storeID, userID =request.user, expected_seller_fulfillment=(timezone.now() + timezone.timedelta(days=5)))
            t.save()
            item.save()
            return JsonResponse({'response' : 'OK!', 'ticketID' : t.ticketID})
        except Exception as e:
            raise e
            return JsonResponse({'error': str(e)}, status=400)







class TicketController(View):

    @staticmethod
    def get_shop_ids(request):
        shopOwner = ShopOwner.objects.filter(userID=request.user).first()
        if shopOwner is None:
            return JsonResponse({'error': 'current user is not a shop owner'}, status=400)
        shop: Store = Store.objects.filter(shopOwnerID=shopOwner).first()
        ticket_result = Ticket.objects.filter(storeID=shop)
        tickets = []
        for ticket in ticket_result:
            shopuser = ShopUser.objects.get(userID=request.user)
            tickets.append(
                {
                    'ticketID': ticket.ticketID,
                    'itemName': ticket.itemID.name,
                    'level / status_id': ticket.status.level,
                    'statusID': ticket.status.statusID,
                    'currentStatusName': ticket.status.status_name,
                    'itemID': ticket.itemID.itemID,
                    'userID': ticket.userID.id,
                    'customerFirstName': ticket.userID.first_name,
                    'customerLastName': ticket.userID.last_name,
                    'customerEmail': ticket.userID.email,
                    'customerPhone': shopuser.phone_no
                }
            )
        return JsonResponse({'tickets': tickets})

    def post(self, request):
        userID = request.POST.get('userID')
        itemID = request.POST.get('itemID')
        userID = User.objects.get(id=userID)
        itemID = Item.objects.get(itemID=itemID)
        print(userID, itemID, 'details')
        if itemID is None:
            return JsonResponse({'error': 'shopUserID and itemID are required'}, status=400)
        Ticket.objects.create(userID=userID, storeID=itemID.storeID, itemID=itemID)
        return JsonResponse({'status': 'OK!'})


    def get(self, request):
        ticket = {}
        ticketID = request.GET.get('ticketID')
        userID = request.GET.get('userID')
        if ticketID is not None:
            ticket_obj: Ticket = Ticket.objects.filter(ticketID=ticketID).first()
            ticket['ticketID'] = ticket_obj.ticketID
            if ticket_obj.status.level == 1:
                if ticket_obj.expected_seller_fulfillment < timezone.now().date():
                    ticket_obj.status = Status.objects.get(statusID=7)
                    ticket_obj.status.save()
                    ticket_obj.save()
            elif ticket_obj.status.level == 2:
                if ticket_obj.expected_buyer_fulfillment < timezone.now().date():
                    ticket_obj.status = Status.objects.get(statusID=8)
                    ticket_obj.status.save()
                    ticket_obj.save()
            ticket['userID'] = ticket_obj.userID.userID.id
            ticket['storeID'] = ticket_obj.storeID.storeID
            ticket['itemID'] = ticket_obj.itemID.itemID
            ticket['createdAt'] = ticket_obj.created
            ticket['expected_seller_fulfillment'] = ticket_obj.expected_seller_fulfillment
            ticket['expected_buyer_fulfillment'] = ticket_obj.expected_buyer_fulfillment
            ## compare dates if it is more than current ime


            status_obj: Status = ticket_obj.status
            if status_obj:
                ticket['status'] = status_obj.status_name
                ticket['statusINT'] = status_obj.level
            else:
                ticket['status'] = "Status not found"
                ticket['statusINT'] = status_obj.level
            return JsonResponse(ticket)
        if userID is not None:
            user = ShopUser.objects.get(id=userID)
            tickets = Ticket.objects.filter(userID=user)
            ticket_list = []
            print(tickets)

            for ticket_obj in tickets:
                ticket_data = {
                    'ticketID': ticket_obj.ticketID,
                    'userID': ticket_obj.userID.userID.id,
                    'storeID': ticket_obj.storeID.storeID,
                    'itemID': ticket_obj.itemID.itemID,
                    'status': ticket_obj.status.status_name,
                    'expected_buyer_fulfillment': ticket_obj.expected_buyer_fulfillment,
                    'expected_seller_fulfillment': ticket_obj.expected_seller_fulfillment,
                    'statusLevel': ticket_obj.status.level,
                    'statusID': ticket_obj.status.statusID

                }
                ticket_list.append(ticket_data)

            return JsonResponse({'tickets': ticket_list})
        else:
            return JsonResponse({'error': 'Invalid parameters'})

    @staticmethod
    def get_statuses(request):
        statuses_set = Status.objects.all()
        statuses = []
        for status in statuses_set:
            statuses.append(
                {
                    'id': status.statusID,
                    'name': status.status_name,
                    'level': status.level
                }
            )
        return JsonResponse({'statuses': statuses})

    @staticmethod
    def update_ticket_status(request):
        if request.method != 'POST':
            return return_not_post()
        sID = request.POST.get('statusID')
        tID = request.POST.get('ticketID')
        if sID is None or tID is None:
            return JsonResponse({'error': 'Invalid parameters'})
        status = Status.objects.get(statusID=sID)
        ticket = Ticket.objects.get(ticketID=tID)
        if status.level == 3:
            print('Now changing to this')
            ticket.itemID.isTaken = 1
            service_fee = float(ticket.itemID.price) * 0.15
            ticket.itemID.storeID.shopOwnerID.balance = float(ticket.itemID.storeID.shopOwnerID.balance) - service_fee
            ticket.itemID.storeID.shopOwnerID.save()
            ticket.itemID.save()
            ticket.save()
        elif status.level == 2:
            ticket.expected_buyer_fulfillment = timezone.now() + timezone.timedelta(days=5)
            ticket.save()
        else:
            ticket.itemID.isTaken = 0
            ticket.itemID.save()
        ticket.save()
        if status is None or ticket is None:
            return JsonResponse({'error': 'Invalid status or ticket IDs'})
        ticket.status = status
        ticket.save()
        return JsonResponse({'success': True})

    @staticmethod
    def drop_ticket(request):
        user = request.user.id
        ticketID = request.POST.get('ticketID')
        ticket: Ticket = Ticket.objects.filter(ticketID=ticketID).first()
        if ticket.userID == user:
            ticket.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
