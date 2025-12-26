import { Insights } from '@chess.com/services/insights/insights.dto';
import { mockResizeObserver } from '@chess.com/utils/tests/mock-resize-observer';
import { render } from '@testing-library/react';
import { InsightsGames } from '..';

describe('InsightsGames', () => {
	beforeEach(() => {
		mockResizeObserver();
	});

	it('to match snapshot', () => {
		const { container } = render(<InsightsGames insights={{} as Insights} />);
		expect(container).toMatchSnapshot();
	});
});
