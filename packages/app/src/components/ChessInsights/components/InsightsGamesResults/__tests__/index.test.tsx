import { Insights } from '@chess.com/services/insights/insights.dto';
import { mockResizeObserver } from '@chess.com/utils/tests/mock-resize-observer';
import { render } from '@testing-library/react';
import { InsightsGamesResults } from '..';

describe('InsightsGamesResults', () => {
	beforeEach(() => {
		mockResizeObserver();
	});

	it('to match snapshot', () => {
		const { container } = render(
			<InsightsGamesResults insights={{} as Insights} />,
		);
		expect(container).toMatchSnapshot();
	});
});
