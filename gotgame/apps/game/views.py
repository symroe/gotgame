import sys
import pusher

from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib import messages


class GameResultView(TemplateView):
    template_name = 'game_result.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            winner = request.POST.get('winner', '1')

            pusher.app_id = '42602'
            pusher.key = '03a4b4dc53485d77490b'
            pusher.secret = '4f0d6a61c3c105ae96d0'

            p = pusher.Pusher()

            p['game'].trigger('end',
                {
                    'winner': winner,
                    '1': {
                        'winner': winner == '1',
                        'credits': 2
                    },
                    '2': {
                        'winner': winner == '2',
                        'credits': 0
                    }
                })
            messages.add_message(request, messages.INFO, 'Successfully notified')
            return redirect('game_result')
        return super(GameResultView, self).dispatch(request, *args, **kwargs)
