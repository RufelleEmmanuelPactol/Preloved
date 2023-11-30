from django.shortcuts import render
from django.views import View
from datetime import datetime
from .models import Ticket, Status
from django.http import JsonResponse
# Create your views here.




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
